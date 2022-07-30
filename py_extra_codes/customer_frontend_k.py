#IMPORTS
import os
import json
from nbformat import write
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import numpy as np
load_dotenv()

#Import supplychaincontracts class
from supply_chain import SupplyChainContract

###NEW LIBARIES
#Import QRcode libary
    #pip install qrcode
import qrcode

    #!pip install opencv-python
import cv2

    #pip install Pillow
from PIL import Image


###Get contract
# load environment variables
load_dotenv()
w3_providerURI = os.getenv("WEB3_PROVIDER_URI")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
path_to_contract = './contracts/compiled/coffeeChain.json'

# Init supply chain contract
coffee_contract = SupplyChainContract(w3_providerURI, path_to_contract, contract_address)

# list of addresses on the testnet
addresses = coffee_contract.w3_provider.eth.accounts

address = st.sidebar.selectbox("owner ETH address", options=addresses)

# button to view node info
if st.button("view node info"):
    node = coffee_contract.get_node(address)
    st.write(node)


st.markdown("View Batch Details")

# set token value to view all events associated with that token
token = st.number_input("Select a Token to View Events", min_value=0)


#view/get info button row
col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    # button to view all nodes a batch has passed through
    if st.button("View the Coffee History", key='viewthecoffeehistory'): #created key otherwise repeated button argument didnt work.
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

with col2:
    # button to view a list of coordinate tuples for each node that the batch passed through
    if st.button("Get Coordinates List", key='getcoordinateslist'):
        st.write(coffee_contract.get_all_cooordinates(token))

with col3:
    # button to view a list of address tuples for each transaction
    if st.button("View All Owner Addresses", key='viewallowneraddresses'):
        st.write(coffee_contract.get_transfer_addresses(token))

with col4:
    # button to view the batch info or URI
    if st.button("View Batch Info", key='viewbatchinfo'):
        st.write(coffee_contract.get_batch_info(token))

#QR Code Code
#QRcode functions and imports

#import csv containing file name, Make sure path is compatible 
qrcode_name = pd.read_csv('file_name.csv')
file_name = qrcode_name['data']

file_name = file_name[0]
file_name = str(file_name) + '.png'

def show_qrcode():
    if st.button("Show QR Code"):
        image = Image.open(file_name)
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



#Coffee code
st.markdown('# Customer and the supply chain')
image = Image.open('images/coffeeee.jpeg')
st.image(image)


#Streamlit web app QR code button functions,
button1, button2, button3 = st.columns([1,1,1])

with button1:
    show_qrcode() #show qr code that was generated

with button2: #read qr code button row
    if st.button('Read last QR code'):
        st.write(read_qrcode(file_name=file_name)) #read the qr code

with button3:
    if st.button('Coffee?'):
        st.balloons()
        st.write('Coffeeeeee!')
