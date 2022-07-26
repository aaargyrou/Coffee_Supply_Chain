import streamlit as st
from supply_chain import SupplyChainContract
import os
from dotenv import load_dotenv
import streamlit as st
from supply_chain import SupplyChainContract

# load environment variables
load_dotenv()
w3_providerURI = os.getenv("WEB3_PROVIDER_URI")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
path_to_contract = './contracts/compiled/coffeeChain.json'

# Init supply chain contract
coffee_contract = SupplyChainContract(w3_providerURI, path_to_contract, contract_address)

# list of addresses on the testnet
addresses = coffee_contract.w3_provider.eth.accounts

st.write("# About us")
for address in addresses:
    node_from = coffee_contract.get_node(address[0])
    node_to = coffee_contract.get_node(address[1])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(node_from)
    with col2:
        st.markdown("# -->")
    with col3:
        st.write(node_to)
