import json
import pandas as pd
import numpy as np
from web3 import Web3
from pathlib import Path

class SupplyChainContract:
    '''
    creates a w3.py contract object with additonal functionality for interacting with the supplychain smart contract.
    '''

    def __init__ (self, web3_provider_URI, contract_json_path, deployed_address):
        self.w3_provider = Web3(Web3.HTTPProvider(web3_provider_URI))
        self.compiled_contract = contract_json_path
        self.address = deployed_address
        self.contract = self.load_contract()

    def load_contract(self):
        '''
        loads a precompiled solidity contract, returns a w3.py contract object
        '''
        # Load the contract ABI from the path to the compiled abi
        with open(Path(self.compiled_contract)) as f:
            contract_abi = json.load(f)

        # return w3 contract object
        return self.w3_provider.eth.contract(address=self.address, abi=contract_abi)

    def populate_supply_chain(self):
        """
        populates the testnet with mock data from the csv files (consumes gas)
        """
        nodes = pd.read_csv('mock_data.csv', index_col= 'index')
        batches = pd.read_csv('mock_batches.csv', index_col= 'index')
        transactions = pd.read_csv('mock_transactions.csv', index_col='Index')

        for row in nodes.index:
            node = nodes.loc[row]
            self.contract.functions.addNode(node[1], node[0], node[4], str(np.floor(node[2])), str(np.floor(node[3]))).transact({'from': node[1], 'gas': 1000000})

        for row in batches.index:
            batch = batches.loc[row]
            self.contract.functions.addBatch(batch[0], "Arabica").transact({'from': batch[0], 'gas': 1000000})

        for row in transactions.index:
            transaction = transactions.loc[row]
            self.contract.functions.transferBatch(transaction[0], transaction[1], int(transaction[2])).transact({'from': transaction[0], 'gas': 1000000})

    def get_all_cooordinates(self, token_number):
        '''
        Gets data from each node visited by a token. 
        Returns a list of tuples with values linked chronologically,
        each tuple represents a coordinate.
        '''
        # create a filter and get all entries filtered by token number
        token_filter = self.contract.events.transfer.createFilter(fromBlock=0, argument_filters={"tokenId": token_number})
        filtered_events = token_filter.get_all_entries()

        # init empty list to hold coordinate tuples.
        coordinates = []

        # loop through all filtered events 
        for x, event in enumerate(filtered_events):
            event_dict = dict(event)

            # because the solidity events trigger only when a transfer happens, we need to access the first node by reading the 'transferFrom' variable.
            if x == 0:
                first_node = self.contract.functions.Nodes(event_dict["args"]["transferFrom"]).call()
                coordinates.append((first_node[2], first_node[3]))

            # append the 3rd and 4th value of the event_dict
            node_data = self.contract.functions.Nodes(event_dict["args"]["transferTo"]).call()
            coordinates.append((node_data[2], node_data[3]))
        return coordinates

    def get_batch_info(self, token_number):
        '''
        gets the URI information about a batch.
        '''
        return self.contract.functions.Batches(token_number).call()

    def get_transfer_addresses(self, token_number):
        '''
        returns a list of tuples, each tuple contains the address from and address to for all transfers of a batch.
        '''
        # init empty list 
        transfers = []

        # filter for given token
        token_filter = self.contract.events.transfer.createFilter(fromBlock=0, argument_filters={"tokenId": token_number})
        reports = token_filter.get_all_entries()

        # loop through all events and append addresses from each event.
        for x, report in enumerate(reports):
            report_dict = dict(report)
            transfer_from = report_dict["args"]["transferFrom"]
            transfer_to = report_dict["args"]["transferTo"]
            transfers.append((transfer_from,transfer_to))
        
        return transfers 

    def send_batch(self, owner, recipient, token_number, gas=1000000):
        '''
        sends a token (representing a batch) from owner to recipient using ERC721 safeTransfer.
        gas limit defaults to 10000000
        '''
        return self.contract.functions.transferBatch(owner, recipient, token_number).transact({'from': owner, 'gas': gas})

    def mint_batch(self, creator_address, batch_uri, gas=1000000):
        '''
        mints a new ERC721 token representing a new batch of goods, attachment of a URI (string) allows for documentation/specifications
        '''
        return self.contract.functions.addBatch(creator_address, batch_uri).transact({'from': creator_address, 'gas': gas})
    
    def get_node(self, address):
        '''
        returns json object containing information about a node associated with an ethereum address
        '''
        return self.contract.functions.Nodes(address).call()
