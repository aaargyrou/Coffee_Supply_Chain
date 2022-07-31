from multiprocessing.sharedctypes import Value
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st
import json
from nbformat import write
from web3 import Web3
from pathlib import Path
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

#Holds data for all transactions
data = []

# load environment variables
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





st.markdown("# The Coffee Supply Chain")
st.markdown(f" ![Alt Text](https://victoryoffices.com.au/wp-content/uploads/2018/11/coffee-productivity-blog.jpg)")
st.markdown("Welcome to the Coffee Supply Chain. This is an ethereum DApp that demonstrates a Supply Chain flow between a Producer and Buyer.  A Producer can add batches of coffee to the inventory system stored in the blockchain. From there the coffee batches can be tracked between their time in storage, at a roasting facility and finally and their designated shop, All visible to the user!!!")
#QRcode functions and imports

#import csv containing file name, Make sure path is compatible 
qrcode_name = pd.read_csv('file_name_example.csv')
file_name = qrcode_name['data']

file_name = file_name[0]
file_name = str(file_name) + '_example.png'

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
#image = Image.open('images/coffeeee.jpeg')
#st.image(image)


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

