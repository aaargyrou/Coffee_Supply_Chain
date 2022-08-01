from importlib.resources import path
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from supply_chain import SupplyChainContract
from PIL import Image


load_dotenv()
w3_providerURI = os.getenv("WEB3_PROVIDER_URI")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
user_address = os.getenv("CONTRACT_USER_ADDRESS")
path_to_contract = '../contracts/compiled/coffeeChain.json'
# Init supply chain contract
coffee_contract = SupplyChainContract(
    w3_providerURI,
    path_to_contract,
    contract_address,
    user_address
    )

# list of addresses on the testnet
addresses = coffee_contract.w3_provider.eth.accounts
#Side BAR
#code here

###Get contract
st.title("Coffee Supply Chain")

# Primary Producer Image
primary_producer_image = Image.open(Path('../images/PrimaryProducerLogo.png'))
storage_image = Image.open(Path('../images/StorageLogo.png'))
roaster_image = Image.open(Path('../images/RoasterLogo.png'))
retailer_image = Image.open(Path('../images/RetailerLogo.png'))
consumer_image = Image.open(Path('../images/ConsumerLogo.png'))

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    # Primary Producer text. Align centre
    st.markdown("Primary Producer")
    # PrimaryProducer png
    st.image(primary_producer_image, width=200)
with col2:
    st.markdown("Storage")
    st.image(storage_image, width=200)
with col3:
    st.markdown("Roaster")
    st.image(roaster_image, width=200)
with col4:
    st.markdown("Retailer")
    st.image(retailer_image, width=200)
with col5:
    st.markdown("Consumer")
    st.image(consumer_image, width=200)

# Description of the admin app
st.header("Description of the app")
st.markdown("Welcome to the Coffee Supply Chain. This is an Ethereum DApp that allows companies to add their business information and coffee batches to the supply chain. The coffee batches, location and transaction history will all be visable to the user through the Customer DApp.")
st.markdown("This Admin App is used to manage the supply chain of coffee. It allows admins to:")
st.markdown("* Add a new Business to the supply chain")
st.markdown("* Add a new batch of coffee to the supply chain")
st.markdown("* Transfer the batch of coffee to the next stage of the supply chain")