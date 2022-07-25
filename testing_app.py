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


# populate whole contract with test data
st.sidebar.markdown("Populate the blockchain with testing data")
if st.sidebar.button("populate with data"):
    coffee_contract.populate_supply_chain()

# streamlit section for testing nodes
st.sidebar.markdown("---")
st.sidebar.markdown("view Node info")
address = st.sidebar.selectbox("owner ETH address", options=addresses)
name = st.sidebar.text_input('name of the node')
node_type = st.sidebar.text_input('node_type (eg: retail)')
latitude = st.sidebar.number_input('node latitude')
longitude = st.sidebar.number_input('node longitude')

if st.sidebar.button("add a node"):
    if coffee_contract.get_node(address):
        st.write("node already exists")
    else:
        coffee_contract.add_node(address, name, node_type, latitude, longitude)
        st.write(f'{coffee_contract.get_node(address)} has been added')

# button to view node info
if st.sidebar.button("view node info"):
    node = coffee_contract.get_node(address)
    st.write(node)

# streamlit section for testing NFT minting
st.sidebar.markdown("---")
st.sidebar.markdown("create a coffee batch")

# variables used in minting a batch
creator = st.sidebar.selectbox("creator", options=addresses)
batch_uri = st.sidebar.text_input("info or URI about batch")

# button for transaction
if st.sidebar.button("mint a new batch NFT"):
    batch = coffee_contract.add_batch(creator, batch_uri)
    st.write(f'batch has been created!\n txn hash: {batch}')


# streamlit section for testing NFT transfers
st.sidebar.markdown("---")
st.sidebar.markdown("send a batch to another address")

# variables used in sending a batch
owner = st.sidebar.selectbox("address from", options=addresses)
to = st.sidebar.selectbox("address to", options=addresses)
batch_num = st.sidebar.number_input("select batch", min_value=0)

# button for transaction
if st.sidebar.button("send a batch"):
    sent_batch = coffee_contract.transfer_batch(owner, to, batch_num)
    if sent_batch:
        st.write(f'batch has been sent\n txn hash: {sent_batch}')


# streamlist section for viewing events
st.sidebar.markdown("---")
st.sidebar.markdown("view batch details")

# set tokn value to view all events associated with that token
token = st.sidebar.number_input("select a token to view events", min_value=0)

# button to view all nodes a batch has passed through
if st.sidebar.button("view the coffee history"):
    addresses = coffee_contract.get_transfer_addresses(token)
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

# button to view a list of coordinate tuples for each node that the batch passed through
if st.sidebar.button("get coordinates list"):
    st.write(coffee_contract.get_all_cooordinates(token))
   
# button to view a list of address tuples for each transaction
if st.sidebar.button("view all owner addresses"):
    st.write(coffee_contract.get_transfer_addresses(token))

# button to view the batch info or URI
if st.sidebar.button("view batch info"):
    st.write(coffee_contract.get_batch_info(token))