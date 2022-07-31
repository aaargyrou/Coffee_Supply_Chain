# Page 1: This page allows an administrator to input the details of their company. 
##Details being the name of the company, the company address, company Longitude and Latitude.
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from supply_chain import SupplyChainContract


# load environment variables
#load_dotenv()
#w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
#user_address = os.getenv("CONTRACT_USER_ADDRESS")
## Get a list of addresses on the testnet
#addresses = w3.eth.accounts
#
##Cache and load main contract 
#@st.cache(allow_output_mutation=True)
#
##load contract function
#def contract_load():
#    #load abi
#    with open(Path('../contracts/compiled/coffeeChain.json')) as f: #compiled json file needs to be called contract_abi.json
#        contract_abi = json.load(f)
#
#    #Get contract address 
#    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
#    
#    #Geting contract
#    contract = w3.eth.contract(
#        address=contract_address,
#        abi=contract_abi
#    )
#    return contract
#
##Load the contract
#contract = contract_load()
load_dotenv()
w3_providerURI = os.getenv("WEB3_PROVIDER_URI")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
user_address = os.getenv("CONTRACT_USER_ADDRESS")
path_to_contract = '../contracts/compiled/coffeeChain.json'

# Init supply chain contract
contract = SupplyChainContract(
    w3_providerURI,
    path_to_contract,
    contract_address,
    user_address
    )

# list of addresses on the testnet
addresses = contract.w3_provider.eth.accounts

# Create a Dataframe
df = pd.DataFrame()

# Title
st.title("Input Business Details")

# Sidebar Input for contract Details
address = st.sidebar.selectbox("Business ETH address", options=addresses)
name = st.sidebar.text_input('Name of Business')
node_type = st.sidebar.selectbox('Business Type', options=['primaryProducer', 'Storage', 'Roaster', 'Retailer','Consumer'])
latitude = st.sidebar.number_input('Business Latitude')
longitude = st.sidebar.number_input('Business Longitude')
coffeebag = st.sidebar.selectbox('Coffeebag', options=['True', 'False'])

# Display the dataframe
if st.sidebar.button("View Details"):
    st.subheader("Contract Details")
    df = df.append(
        {'address': address, 'name': name, 'node_type': node_type, 'lat': latitude, 'lon': longitude, 'coffeebag': coffeebag}, ignore_index=True)
    st.write(df)

    # MAPBOX for Longitude and Latitude 
    st.map(df)

#TODO BUTTON TO LINK TO SMART CONTRACT AND STORE DATA IN THE BLOCKCHAIN

if st.button("Add Business"):
    df = df.append(
        {'address': address, 'name': name, 'node_type': node_type, 'lat': latitude, 'lon': longitude, 'coffeebag': coffeebag}, ignore_index=True)
    st.write(df)
    st.map(df)
    contract.add_node(address, name, node_type, latitude, longitude)
    st.write(f'{contract.get_node(address)} has been added to the Smart Contract')