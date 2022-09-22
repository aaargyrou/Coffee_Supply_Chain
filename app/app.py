import streamlit as st
import os
from dotenv import load_dotenv
from supply_chain import SupplyChainContract

# load environment vairables
load_dotenv()
ss = st.session_state

if "w3_providerURI" not in ss:
    ss.w3_providerURI = os.getenv("WEB3_PROVIDER_URI")

if "contract_address" not in ss:
    ss.contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

if "user_address" not in ss:
    ss.user_address = os.getenv("CONTRACT_USER_ADDRESS")

if "path_to_contract" not in ss:
    ss.path_to_contract = "../contracts/compiled/coffeeChain.json"

if "openweathermapAPIkey" not in ss:
    ss.openweathermapAPIkey = os.getenv("OPEN_WEATHER_MAP_API_KEY")

# Init session state variables
if "contract" not in ss:
    ss.contract = SupplyChainContract(
        ss.w3_providerURI, ss.path_to_contract, ss.contract_address, ss.user_address
    )

st.markdown(
    f" ![Alt Text](https://victoryoffices.com.au/wp-content/uploads/2018/11/coffee-productivity-blog.jpg)"
)
st.markdown(
    "Welcome to the Coffee Supply Chain. This is an ethereum DApp that demonstrates a Supply Chain flow between a Producer and Buyer.  A Producer can add batches of coffee to the inventory system stored in the blockchain. From there the coffee batches can be tracked between their time in storage, at a roasting facility and finally and their designated shop, All visible to the user!!!"
)
