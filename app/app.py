import streamlit as st
import os
from dotenv import load_dotenv
from supply_chain import SupplyChainContract

# load environment vairables
load_dotenv()
w3_providerURI = os.getenv("WEB3_PROVIDER_URI")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
user_address = os.getenv("CONTRACT_USER_ADDRESS")
path_to_contract = "../contracts/compiled/coffeeChain.json"

# Init supply chain contract
if "contract" not in st.session_state:
    st.session_state.contract = SupplyChainContract(
        w3_providerURI, path_to_contract, contract_address, user_address
    )

st.markdown(
    f" ![Alt Text](https://victoryoffices.com.au/wp-content/uploads/2018/11/coffee-productivity-blog.jpg)"
)
st.markdown(
    "Welcome to the Coffee Supply Chain. This is an ethereum DApp that demonstrates a Supply Chain flow between a Producer and Buyer.  A Producer can add batches of coffee to the inventory system stored in the blockchain. From there the coffee batches can be tracked between their time in storage, at a roasting facility and finally and their designated shop, All visible to the user!!!"
)
