# Page 1: This page allows an administrator to input the details of their company. 
##Details being the name of the company, the company address, company Longitude and Latitude.
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

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

# Read all data inputed above
with st.sidebar("Loading Contract Details"):
    with st.spinner("Loading Contract Details"):
        contract_details = w3.eth.get_contract_details(contract, address)
