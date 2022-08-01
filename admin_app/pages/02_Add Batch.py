from audioop import add
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from PIL import Image
import cv2
import qrcode
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
df = pd.DataFrame()

# Title
st.title("Add Batch")
st.markdown("---")

# Input Batch Information
gas = 1000000

st.sidebar.text_input("Enter Batch Number")
creator_address = st.sidebar.selectbox("owner address", options=addresses)
batch_uri = st.sidebar.text_input("Batch URI")
value_eth = st.sidebar.number_input("Enter Batch Value (ETH)")
batch_state = st.sidebar.selectbox("Batch State", [True, False])

if st.sidebar.button("View Details"):
    st.subheader("Contract Details")
    df = df.append(
        {'creator_address': creator_address, 
            'batch_uri': batch_uri, 
            'value_wei': value_eth,
            'batch_state': batch_state}, ignore_index=True)
    st.write(df)

# Button to add data to contract
if st.button("Add Batch"):
    # use addBatch function to add batch to contract
    df = df.append(
        {'creator_address': creator_address, 
            'batch_uri': batch_uri, 
            'value_wei': value_eth,
            'batch_state': batch_state}, ignore_index=True)
    batch = contract.add_batch(creator_address, batch_uri, value_eth, batch_state)
    st.write(df)
    st.write(f'Batch has been created!\n txn hash: {batch}')

################################################################
def generate_qrcode(input_str, file_name):
#Generate QR code
    qr_img = qrcode.make(input_str)  
#Save image file   
    qr_img.save(file_name+'.png')
    file_name_ = file_name+'.png'
    return qr_img, file_name_

#Show and read QR code function

def show_qrcode():
    if st.button("Show QR Code"):
        image = Image.open(qr_CODE[1])
        st.image(image, caption='Your QRcode (try reading it with your phone camera)')


#Read QR code function
def read_qrcode(file_name):
#load/read image
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


#Streamlit QR code generator inputs and buttons

### potentually change QR code inputs to token ids or any backend data
st.markdown('# Generate a QR Code')
# qr_code_content select box with batch's data
qr_code_content = st.text_input('Enter Streamlit Web App link')
qr_code_filename = st.text_input('QR code "File Name"')

qr_CODE = generate_qrcode(qr_code_content, qr_code_filename)

#save file name as a csv to be accessed by the customer app
file_name_data = pd.DataFrame({'data': [qr_code_filename]})
file_name_data.to_csv('file_name.csv', index=False) ##Saved csv LOCATION is important as customer_frontend app must access the data

#Streamlit web app QR code button functions
button1, button2 = st.columns([1,1])

with button1:
    show_qrcode() #show qr code that was generated

with button2: #read qr code button row
    if st.button('Read last QR code'):
        st.write(read_qrcode(file_name=qr_CODE[1])) #read the qr code

######################################