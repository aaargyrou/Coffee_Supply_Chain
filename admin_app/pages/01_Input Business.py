# Page 1: This page allows an administrator to input the details of their company. 
##Details being the name of the company, the company address, company Longitude and Latitude.
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

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

#if st.sidebar.button("Add Business"):
#    contract.functions.addNode(address, name, node_type, latitude, longitude).transact({'from': user_address})
#    st.write("Business added")



# variables used in minting a batch
# creator = st.selectbox("creator", options=addresses)
# batch_uri = st.text_input("info or URI about batch")

# button for transaction
# if st.sidebar.button("mint a new batch NFT"):
#    batch = coffee_contract.add_batch(creator, batch_uri)
#    st.write(f'batch has been created!\n txn hash: {batch}')