# Page 1: This page allows an administrator to input the details of their company. 
##Details being the name of the company, the company address, company Longitude and Latitude.
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Add Functions
def get_node(self, address):
        '''
        returns json object containing information about a node associated with an ethereum address
        '''
        return self.contract.functions.Nodes(address).call()

def add_node(self, node_address, name, type, latitude, longitude, gas=1000000):
    '''
    adds a node to the contract (consumes gas)
    Args:
        address (string): 42-character hexadecimal address associated with the ethereum blockchain
        name (string): name of the node
        type (string): function or operation that this node performs in the supplychain
        latitude (float/int): latitude of the node
        longitude (float/int): longitude of the node
        gas (int): maximum gas to consume during transaction
    '''
    return self.contract.functions.addNode(node_address, name, type, str(latitude), str(longitude)).transact({'from': self.user, 'gas': gas})

# load environment variables
load_dotenv()
user_address = os.getenv("CONTRACT_USER_ADDRESS")
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
# Get a list of addresses on the testnet
addresses = w3.eth.accounts

#Cache and load main contract 
@st.cache(allow_output_mutation=True)

#load contract function
def contract_load():
    #load abi
    with open(Path('../contracts/compiled/coffeeChain.json')) as f: #compiled json file needs to be called contract_abi.json
        contract_abi = json.load(f)

    #Get contract address 
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    
    #Geting contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    return contract

#Load the contract
contract = contract_load()

# Title
st.title("Input Node")

# Text Input for contract Details
st.subheader("Contract Details")


address = st.selectbox("Business ETH address", options=addresses)
name = st.text_input('Name of Business')
node_type = st.selectbox('Business Type', options=['primaryProducer', 'Storage', 'Roaster', 'Retailer','Consumer'])
latitude = st.number_input('Business Latitude')
longitude = st.number_input('Business Longitude')

# Add inputed data to Contract
if st.button("Add"):
    if 