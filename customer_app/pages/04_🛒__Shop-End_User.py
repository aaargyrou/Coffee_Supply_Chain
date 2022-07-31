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



st.markdown("# Shops")
st.markdown(f"### These Coffee beans were sold in {data[3][0]}")
###### CODE FOR MAPBOX ######
lat = float(data[3][2])
lon = float(data[3][3])


df = pd.DataFrame(
     [[lat, lon]],
     columns=['lat', 'lon'])

st.map(df)
###### --------------- ######

st.markdown("### Common Advice")
st.markdown("Once you’ve cracked open the bag, here’s some tips to help you best store your beans for maximum flavour and lifespan.")
st.markdown("# * Use an airtight container")
st.markdown("Keeping the beans in resealable bags so that the air around the coffee sealed so it doesn’t get exposed to fresh air and oxidise quickly. If you’d prefer, you can transfer the beans to a small, opaque, airtight container. It doesn’t need to have fancy valves: after 2-3 days most of the roast gases will have escaped the bag we packed the coffee into.")
st.markdown("# * Grind it as you brew")
st.markdown("It’s the oils and moisture in the coffee bean that gives you a delicious cup of coffee: but they both also react with air over time. That’s why we recommend grinding your coffee just before you brew, so all that flavour goes into your cup, not into the air.")
st.markdown("# * Cool, dark place.")
st.markdown("Once you’re storing the coffee in an airtight container, the other two things that can speed up its ageing are exposure to light, and heat. Easy fix: store your coffee in a cool, dark, dry place (but not the fridge).")
