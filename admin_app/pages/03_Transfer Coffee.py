import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from decimal import Decimal
from supply_chain import SupplyChainContract

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

# Title (Transfer Coffee Batch)
st.title("Transfer Coffee Batch")
st.markdown("---")

# variables used in sending a batch
owner = st.selectbox("Your Address", options=addresses)
to = st.selectbox("Send to address", options=addresses)
# Select a batch to transfer
batch_num = st.number_input("Batch Number", min_value=0)

# Button to view transaction details
if st.button("Approve transfer of a batch"):
    approval = contract.approve_transfer(owner, to, batch_num)
    if approval:
        st.write(f'Batch has been sent\n txn hash: {approval}')
    else:
        st.write("Batch not sent")


# Button to view transaction details
if st.button("Send Coffee Batch"):
    sent_batch = contract.transfer_batch(owner, to, batch_num)
    if sent_batch:
        st.write(f'Batch has been sent\n txn hash: {sent_batch}')
    else:
        st.write("Batch not sent")

# streamlist section for viewing events
st.header("View Batch Details")

# button to view all nodes a batch has passed through
if st.button("View the Coffee History"):
    addresses = contract.get_transfer_addresses(batch_num)
    for address in addresses:
        node_from = contract.get_node(address[0])
        node_to = contract.get_node(address[1])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(node_from)
        with col2:
            st.markdown("# -->")
        with col3:
            st.write(node_to)


