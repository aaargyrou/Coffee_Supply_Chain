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
owner = st.selectbox("address from", options=addresses)
to = st.selectbox("address to", options=addresses)
# Select a batch to transfer
batch_num = st.number_input("Batch Number", min_value=0)

# Button to view transaction details
if st.button("View Details"):
    st.button("View Transaction Details", button_data=json.dumps({
        "type": "transactionDetails",
        "owner": owner,
        "to": to,
        "batch_num": batch_num
    }))


# button for transaction
if st.button("Transfer Batch"):
    sent_batch = contract.transfer_batch(owner, to, batch_num)
    if sent_batch:
        st.write(f'batch has been sent\n txn hash: {sent_batch}')