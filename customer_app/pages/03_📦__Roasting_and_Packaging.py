from multiprocessing.sharedctypes import Value
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st
from supply_chain import SupplyChainContract

#Holds data for all transactions
data = []

# load environment variables
load_dotenv()
w3_providerURI = os.getenv("WEB3_PROVIDER_URI")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
user_address = os.getenv("CONTRACT_USER_ADDRESS")
path_to_contract = './contracts/compiled/coffeeChain.json'

# Init supply chain contract
coffee_contract = SupplyChainContract(
    w3_providerURI,
    path_to_contract,
    contract_address,
    user_address
    )

# list of addresses on the testnet
addresses = coffee_contract.w3_provider.eth.accounts

#token = st.sidebar.number_input("select a token to view events", min_value=int(0))
token = st.sidebar.radio(
     "Which batch would you like to track?",
     (0, 1))


# This is to avoid bugs so that even if no batch is chosen there will always be a token assosiated
if token == 0:
     addresses = coffee_contract.get_transfer_addresses(0)
elif token == 1:
     addresses = coffee_contract.get_transfer_addresses(1)
else:
     addresses = coffee_contract.get_transfer_addresses(0)

for address in addresses:
     node_from = coffee_contract.get_node(address[0])
     node_to = coffee_contract.get_node(address[1])
     data.append(node_from)






#st.write(data)


st.markdown("# Roasting and Packaging Facilities")
st.markdown(f"### These beans were roasted and packaged in {data[2][0]}")
###### CODE FOR MAPBOX ######
lat = float(data[2][2])
lon = float(data[2][3])


df = pd.DataFrame(
     [[lat, lon]],
     columns=['lat', 'lon'])

st.map(df)
###### --------------- ######

st.markdown("### How is Coffee Roasted?")
st.markdown("Raw coffee beans are dropped into loaders and then into a rotating drum. The drum is pre-heated to a temperature of around 240 degrees. After 12-15 minutes depending on the type of roast, the roasted beans will exit the drum at around 195 degrees and are then taken out into a cooling tray at the front of the roaster.")


