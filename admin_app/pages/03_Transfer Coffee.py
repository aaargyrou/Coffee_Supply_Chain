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

# variables used in sending a batch
owner = st.selectbox("address from", options=addresses)
to = st.selectbox("address to", options=addresses)
batch_num = st.number_input("select batch", min_value=0)

# button for transaction
if st.button("send a batch"):
    sent_batch = contract.functions.transferBatch(owner, to, batch_num)
    if sent_batch:
        st.write(f'batch has been sent\n txn hash: {sent_batch}')
