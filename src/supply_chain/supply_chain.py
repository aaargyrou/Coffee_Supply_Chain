import re
import json
import pandas as pd
from web3 import Web3
from pathlib import Path
from decimal import Decimal


class SupplyChainContract:
    """
    creates a w3.py contract object with additonal functionality for interacting with the supplychain smart contract.
    User address determines accessable functions when calling some of the transactional functions.
    Refer to the deployed smart contract for user permissions.

    Args:
        web3_provider_URI (string): HTTP URI to the web3 provider
        contract_json_path (string): path to the compiled contract abi.json
        deployed_address (string): 42-character hexadecimal address for the deployed contract
        user_address (string):  42-character hexadecimal address for the user of the SupplyChainContract
    """

    def __init__(
        self, web3_provider_URI, contract_json_path, deployed_address, user_address
    ):
        self.w3_provider = Web3(Web3.HTTPProvider(web3_provider_URI))
        self.compiled_contract = contract_json_path
        self.address = deployed_address
        self.contract = self.load_contract()
        self.user = user_address

    def load_contract(self):
        """
        loads a precompiled solidity contract, returns a w3.py contract object
        """
        # Load the contract ABI from the path to the compiled abi
        with open(Path(self.compiled_contract)) as f:
            contract_abi = json.load(f)

        # return w3 contract object
        return self.w3_provider.eth.contract(address=self.address, abi=contract_abi)

    def map_data(self, token_id):
        """
        Gets map data from each node visited by a token.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        Returns:
            A pandas dataframe containing node info in chronological order.
        """
        filtered_events = self.get_filtered_events(token_id)

        # init empty list to hold coordinate tuples.
        map_data = []

        # loop through all filtered events
        for x, event in enumerate(filtered_events):
            event_dict = dict(event)

            # because the solidity events trigger only when a transfer happens, we need to access the first node by reading the 'transferFrom' variable.
            if x == 0:
                node_data = self.contract.functions.Nodes(
                    event_dict["args"]["transferFrom"]
                ).call()
                map_data.append(node_data)

            # append the reamining values of the event_dict
            node_data = self.contract.functions.Nodes(
                event_dict["args"]["transferTo"]
            ).call()
            map_data.append(node_data)

        map_data = (
            pd.DataFrame(map_data)
            .rename(columns={0: "name", 1: "category", 2: "latitude", 3: "longitude"})
            .drop(columns=[4])
        )
        return map_data.astype({"latitude": float, "longitude": float})

    def get_filtered_events(self, token_id):
        """
        Gets the events for transfers for a tokenId.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        Returns:
            dict of events from the Transfers event filtered by tokenId
        """
        # create a filter and get all entries filtered by token number
        token_filter = self.contract.events.transfer.createFilter(
            fromBlock=0, argument_filters={"tokenId": token_id}
        )
        return token_filter.get_all_entries()

    def get_transfer_logs(self, token_id):
        """
        Gets the logs for transfers for a tokenId.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        Returns:
            dict of logs from the Transfers event filtered by tokenId
        """
        logs = self.contract.events.Transfer.getLogs(
            fromBlock=0, argument_filters={"tokenId": token_id}
        )
        return logs

    def get_transfer_transactions(self, token_id):
        """
        builds a pandas dataframe of all Transactions for a batch

        Args:
            token_id (int): unique token identificaiton number representing the batch
        Returns:
            pands dataframe of all transactions from the Transfers event filtered by tokenId
        """
        df = pd.DataFrame()
        logs = self.get_transfer_logs(token_id)

        for log in logs:
            txn_hash = log["transactionHash"]
            txn = pd.DataFrame([self.w3_provider.eth.getTransaction(txn_hash)])
            df = df.append(txn)
        return df

    def get_transfer_receipts(self, token_id):
        """
        builds a pandas dataframe of all Transaction receipts for a batch

        Args:
            token_id (int): unique token identificaiton number representing the batch
        Returns:
            pands dataframe of all transaction receipts from the Transfers event filtered by tokenId
        """
        df = pd.DataFrame()
        logs = self.get_transfer_logs(token_id)

        for log in logs:
            rcp_hash = log["transactionHash"]
            rcp = pd.DataFrame([self.w3_provider.eth.getTransactionReceipt(rcp_hash)])
            df = df.append(rcp)
        return df

    def value_breakdown(self, token_id):
        """
        combines transaction values and transaction receipts to see batch and gas value for all transactions associated with a transfer, filtered by batch.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        Returns:
            pands dataframe of values and gas costs filtered by tokenId
        """
        tnf = self.get_transfer_transactions(token_id)
        rcp = self.get_transfer_receipts(token_id)
        val = tnf[["from", "hash", "value"]].set_index("hash")
        gas = rcp[["transactionHash", "gasUsed"]].set_index("transactionHash")
        values = pd.concat([val, gas], join="inner", axis=1)
        return values

    def get_batch_URI(self, token_id):
        """
        gets the URI information about a batch.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        """
        return self.contract.functions.tokenURI(token_id).call()

    def get_transfer_addresses(self, token_id):
        """
        gets a list of tuples, each tuple contains the address from and address to for all transfers of a batch.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        """
        filtered_events = self.get_filtered_events(token_id)

        # init empty list
        transfers = []

        # loop through all events and append addresses from each event.
        for x, event in enumerate(filtered_events):
            report_dict = dict(event)
            transfer_from = report_dict["args"]["transferFrom"]
            transfer_to = report_dict["args"]["transferTo"]
            transfers.append((transfer_from, transfer_to))

        return transfers

    def transfer_batch(self, owner, recipient, token_id, gas=1000000):
        """
        sends a token (representing a batch) from owner to recipient using ERC721 safeTransfer.

        Args:
            owner (string): 42-character hexadecimal address associated with the ethereum blockchain
            recipient (string): 42-character hexadecimal address associated with the ethereum blockchain
            token_id (int): unique token identificaiton number representing the batch
            gas (int): maximum gas to consume during transaction
        """
        batch_value = self.contract.functions.getBatchValue(token_id).call()
        return self.contract.functions.transferBatch(owner, token_id).transact(
            {"from": recipient, "value": batch_value, "gas": gas}
        )

    def add_batch(
        self, creator_address, batch_uri, batch_value, batch_state=False, gas=1000000
    ):
        """
        mints a new ERC721 token representing a new batch of goods.

        Args:
            creator_address (string): 42-character hexadecimal address associated with the ethereum blockchain
            batch_uri (string): URI to documentation/specifications or batch attributes
            batch_value (int): value of the batch token in ETH (value converted to wei before transacting)
            batch_state (bool): boolean value to determine if a batch is ready for transfer or not (true enables transfers, default to False)
        """
        value_wei = Web3.toWei(Decimal(batch_value), "ether")
        return self.contract.functions.addBatch(
            creator_address, batch_uri, value_wei, batch_state
        ).transact({"from": creator_address, "gas": gas})

    def get_node(self, address):
        """
        get information about a node in the supplychain

        Args:
            address (string): 42-character hexadecimal address to the node

        Returns:
            json object containing information about a node associated with an ethereum address
        """
        return self.contract.functions.Nodes(address).call()

    def add_node(self, node_address, name, type, latitude, longitude, gas=1000000):
        """
        adds a node to the contract (consumes gas)

        Args:
            address (string): 42-character hexadecimal address associated with the ethereum blockchain
            name (string): name of the node
            type (string): function or operation that this node performs in the supplychain
            latitude (float/int): latitude of the node
            longitude (float/int): longitude of the node
            gas (int): maximum gas to consume during transaction
        """
        return self.contract.functions.addNode(
            node_address, name, type, str(latitude), str(longitude)
        ).transact({"from": self.user, "gas": gas})

    def set_batch_state(self, state, token_id, gas=1000000):
        """
        sets the boolean state of a batch, user address pays for gas.

        Args:
            state (bool): boolean value to determine if a batch is ready for transfer or not (true enables transfers)
            token_id (int): unique token identificaiton number representing the batch
            gas (int): maximum gas to consume during transaction
        """
        return self.contract.functions.setBatchState(state, token_id).transact(
            {"from": self.user, "gas": gas}
        )

    def set_batch_value(self, value, token_id, gas=1000000):
        """
        sets the value of a batch, user address pays for gas.

        Args:
            value (int): value of the batch token in ETH (value converted to wei before transacting)
            token_id (int): unique token identificaiton number representing the batch
            gas (int): maximum gas to consume during transaction
        """
        value_wei = Web3.toWei(Decimal(value), "ether")
        return self.contract.functions.setBatchValue(value_wei, token_id).transact(
            {"from": self.user, "gas": gas}
        )

    def get_batch_value(self, token_id):
        """
        gets the value of a batch

        Args:
            token_id (int): unique token identificaiton number representing the batch

        Returns:
            float: value of batch in ETH.
        """
        value_wei = self.contract.functions.getBatchValue(token_id).call()

        return Web3.fromWei(value_wei, "ether")

    def get_batch_state(self, token_id):
        """
        gets the state of a batch to determine if the batch is ready for transfer or not.

        Args:
            token_id (int): unique token identificaiton number representing the batch

        Returns:
            bool: state of a batch (true represents batch is ready for transfer)
        """
        return self.contract.functions.getBatchState(token_id).call()

    def approve_transfer(
        self, owner_address, address_to_approve, token_id, gas=1000000
    ):
        """
        allows a batch owner to approve a buyer for transfer of the batch to a new node

        Args:
            address (string): 42-character hexadecimal address to be approved
            token_id (int): unique token identificaiton number representing the batch
            gas (int): maximum gas to consume during transaction
        """
        self.set_batch_state(True, token_id)
        return self.contract.functions.approve(address_to_approve, token_id).transact(
            {"from": owner_address, "gas": gas}
        )

    def get_batch_owner(self, batch_number):
        """
        returns the address of the owner of a batch

        Args:
            batch_number (int): integer relating to a batch
        """
        return self.contract.functions.ownerOf(batch_number).call()

    def batch_geoJSON(self, batch_number):
        """
        constructs a geoJson object for the travel path of a batch along its nodes.

        Args:
            batch_number(int): integer relating to batch
        """
        # get all coordinates from contract function
        coords = self.map_data(batch_number)
        coords = list(zip(coords["longitude"], coords["latitude"]))

        # construct dict for json
        geoJSON = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": coords},
                    "properties": {},
                },
            ],
        }
        return geoJSON

    def total_supply(self):
        """
        returns total supply of batches
        """
        return self.contract.functions.totalSupply.call()

    def all_batches_owned_by(self, address):
        """
        returns information of all batches owned by an address

        Args:
            owner_address(string): 42-character hexadecimal address

        Returns: list of batch numbers owned by the given address
        """
        amount_owned_by = self.contract.functions.balanceOf(address).call()
        owned_batches = []
        index = 0
        while len(owned_batches) < amount_owned_by:
            batch = self.contract.functions.tokenOfOwnerByIndex(address, index).call()
            owned_batches.append(batch)
            index += 1
        return owned_batches
