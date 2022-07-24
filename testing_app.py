import os
import json
import pandas as pd
import numpy as np
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import time

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
    populates the testnet with mock data from the csv files
    """
    nodes = pd.read_csv('mock_data.csv', index_col= 'index')
    batches = pd.read_csv('mock_batches.csv', index_col= 'index')
    transactions = pd.read_csv('mock_transactions.csv', index_col='Index')

    for row in nodes.index:
        node = nodes.loc[row]
        coffee_chain_contract.functions.addNode(node[1], node[0], node[4], str(np.floor(node[2])), str(np.floor(node[3]))).transact({'from': node[1], 'gas': 1000000})

    for row in batches.index:
        batch = batches.loc[row]
        coffee_chain_contract.functions.addBatch(batch[0], "Arabica").transact({'from': batch[0], 'gas': 1000000})

    for row in transactions.index:
        transaction = transactions.loc[row]
        coffee_chain_contract.functions.transferBatch(transaction[0], transaction[1], int(transaction[2])).transact({'from': transaction[0], 'gas': 1000000})

# load the contract
coffee_chain_contract = load_contract("coffeeChain")

# list of addresses on the testnet
addresses = w3.eth.accounts


# populate whole contract with test data
st.sidebar.markdown("Populate the blockchain with testing data")
if st.sidebar.button("populate with data"):
    populate_supply_chain()

# streamlit section for testing nodes
st.sidebar.markdown("---")
st.sidebar.markdown("view Node info")
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

    if reports:
        for x, report in enumerate(reports):
            report_dict = dict(report)
            transfer_from = report_dict["args"]["transferFrom"]
            transfer_to = report_dict["args"]["transferTo"]
            supply_chain_from = coffee_chain_contract.functions.Nodes(transfer_from).call()
            supply_chain_to = coffee_chain_contract.functions.Nodes(transfer_to).call()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(supply_chain_from)
            with col2:
                st.markdown("# -->")
            with col3:
                st.write(supply_chain_to)
    else:
        st.write("This batch has not moved from its place of origin.")

