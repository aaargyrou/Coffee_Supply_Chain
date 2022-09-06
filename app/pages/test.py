import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supply_chain import SupplyChainContract

# load environment vairables
load_dotenv()
w3_providerURI = os.getenv("WEB3_PROVIDER_URI")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
user_address = os.getenv("CONTRACT_USER_ADDRESS")
path_to_contract = "../contracts/compiled/coffeeChain.json"

# Init supply chain contract
contract = SupplyChainContract(
    w3_providerURI, path_to_contract, contract_address, user_address
)

if st.button("Coffee?"):
    contract.populate_supply_chain(
        "../tests/test_nodes.csv",
        "../tests/test_batches.csv",
        "../tests/test_transactions.csv",
    )
    st.balloons()
    st.write("Coffeeeeee!")


# Read QR code function
def read_qrcode(file_name):
    # load/read image
    image = cv2.imread(file_name)
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    # detect and decode
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    # if there is a QR code
    # write/display the data
    if vertices_array is not None:
        st.write("QRCode data:")
        st.write(data)
    else:
        st.write("There was some error")
