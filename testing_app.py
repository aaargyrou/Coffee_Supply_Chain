import os
import json
import pandas as pd
import numpy as np
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# load environment variables
load_dotenv()

# Init web3 provider connection
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@st.cache(allow_output_mutation=True)
def load_contract(abi_json):
    '''
    loads a precompiled solidity contract, returns a w3.py contract object
    '''

    # Load the contract ABI
    with open(Path(f'./contracts/compiled/{abi_json}.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

def populate_supply_chain():
    """
    populates the testnet with mock data from the csv file
    """
    df = pd.read_csv('mock_data.csv', index_col= 'index')
    for row in df.index:
        data = df.loc[row]
        coffee_chain_contract.functions.addNode(data[1], data[0], data[4], str(np.floor(data[2])), str(np.floor(data[3]))).transact({'from': data[1], 'gas': 1000000})


# load the contract
coffee_chain_contract = load_contract("coffeeChain")

# list of addresses on the testnet
addresses = w3.eth.accounts


# streamlit section for testing nodes
st.sidebar.markdown("Populate the blockchain")
if st.sidebar.button("populate with data"):
    populate_supply_chain()

address = st.sidebar.selectbox("owner ETH address", options=addresses)

if st.sidebar.button("view node info"):
    node = coffee_chain_contract.functions.Nodes(address).call()
    st.write(node)


# streamlit section for testing NFT minting
st.sidebar.markdown("---")
st.sidebar.markdown("create a coffee batch")

creator = st.sidebar.selectbox("creator", options=addresses)
batch_uri = st.sidebar.text_input("info or URI about batch")

if st.sidebar.button("mint a new batch NFT"):
    batch = coffee_chain_contract.functions.addBatch(creator, batch_uri).transact({'from': creator, 'gas': 1000000})
    st.write(batch)


# streamlit section for testing NFT transfers
st.sidebar.markdown("---")
st.sidebar.markdown("send a batch to another address")

all_tokens = coffee_chain_contract.functions.totalSupply().call()

owner = st.sidebar.selectbox("address from", options=addresses)
to = st.sidebar.selectbox("address to", options=addresses)
batch_num = st.sidebar.number_input("select batch", min_value=0, max_value=all_tokens)

if st.sidebar.button("send a batch"):
    sent_batch = coffee_chain_contract.functions.transferBatch(owner, to, batch_num).transact({'from': owner, 'gas': 1000000})
    st.write(sent_batch)


# streamlist section for viewing events
st.sidebar.markdown("---")
st.sidebar.markdown("view batch events")

batch_filter = st.sidebar.number_input("select batch to filter by", min_value=0, max_value=all_tokens)

if st.sidebar.button("view the coffee events"):
    appraisal_filter = coffee_chain_contract.events.transfer.createFilter(fromBlock=0, argument_filters={"tokenId": batch_filter})
    reports = appraisal_filter.get_all_entries()
    st.write(reports)

