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

    def populate_supply_chain(self, node_data_path, batch_data_path, txn_data_path):
        """
        populates the testnet with mock data from the csv files (consumes gas)

        Args:
            node_data_path (string): path to node data csv, columns=[index, Business_names, Business_adresses, Latitude, Longitude, node_type]
            batch_data_path (string): path to batch data csv, column=[index, Creator_address, URI, Value, State]
            txn_data_path (string): path to transaction data csv, columns=[index, From_address, To_address, batch_num]
        """
        nodes = pd.read_csv(node_data_path, index_col="index")
        batches = pd.read_csv(batch_data_path, index_col="index")
        transactions = pd.read_csv(txn_data_path, index_col="index")

        # Add all data in nodes to the testnet
        for index, node in nodes.iterrows():
            self.add_node(node[1], node[0], node[4], node[2], node[3])

        for index, batch in batches.iterrows():
            self.add_batch(batch[0], batch[1], batch[2], batch[3])

        for index, transaction in transactions.iterrows():
            # due to default false batch state, batch states need to be set to true before transactions occur
            self.set_batch_state(True, int(transaction[2]))

            # approvals for transfer also need to be set to allow transfer of the NFT
            self.approve_transfer(transaction[0], transaction[1], int(transaction[2]))
            self.transfer_batch(transaction[0], transaction[1], int(transaction[2]))

    def get_all_cooordinates(self, token_id):
        """
        Gets coordinate data from each node visited by a token.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        Returns:
            A list of tuples with values linked chronologically, each tuple represents a coordinate.
        """
        # create a filter and get all entries filtered by token number
        token_filter = self.contract.events.transfer.createFilter(
            fromBlock=0, argument_filters={"tokenId": token_id}
        )
        filtered_events = token_filter.get_all_entries()

        # init empty list to hold coordinate tuples.
        coordinates = []

        # loop through all filtered events
        for x, event in enumerate(filtered_events):
            event_dict = dict(event)

            # because the solidity events trigger only when a transfer happens, we need to access the first node by reading the 'transferFrom' variable.
            if x == 0:
                first_node = self.contract.functions.Nodes(
                    event_dict["args"]["transferFrom"]
                ).call()
                coordinates.append((float(first_node[2]), float(first_node[3])))

            # append the reamining values of the event_dict
            node_data = self.contract.functions.Nodes(
                event_dict["args"]["transferTo"]
            ).call()
            coordinates.append((float(node_data[2]), float(node_data[3])))
        return coordinates

    def get_batch_info(self, token_id):
        """
        gets the URI information about a batch.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        """
        return self.contract.functions.Batches(token_id).call()

    def get_transfer_addresses(self, token_id):
        """
        gets a list of tuples, each tuple contains the address from and address to for all transfers of a batch.

        Args:
            token_id (int): unique token identificaiton number representing the batch
        """
        # init empty list
        transfers = []

        # filter for given token
        token_filter = self.contract.events.transfer.createFilter(
            fromBlock=0, argument_filters={"tokenId": token_id}
        )
        reports = token_filter.get_all_entries()

        # loop through all events and append addresses from each event.
        for x, report in enumerate(reports):
            report_dict = dict(report)
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
        coords = self.get_all_cooordinates(batch_number)
        coord_list = [[x[1], x[0]] for x in coords]

        # construct dict for json
        geoJSON = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": coord_list},
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
