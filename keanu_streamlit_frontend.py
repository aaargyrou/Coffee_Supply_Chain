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


#SHOULD PUT SIDEBAR INTO ITS OWN PAGE NAVIGATOR?


# populate whole contract with test data
st.sidebar.markdown("Populate the Blockchain with Testing Data")
if st.sidebar.button("Populate with Data"):
    coffee_contract.populate_supply_chain()

# streamlit section for testing nodes
st.sidebar.markdown("---")
st.sidebar.markdown("View Node info")
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

    ###MAKE ON MAIN PAGEe

#st.sidebar.markdown("view batch details")

# set token value to view all events associated with that token
token = st.number_input("select a token to view events", min_value=0)


#view/get info button row
col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    # button to view all nodes a batch has passed through
    if st.button("View the Coffee History", key='viewthecoffeehistory'):
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


#Contract Inputs

#Buttons to call contract Functions in streamlit

 ######
#URI
#get uri code function from instruactor code
#coffee packaging would have a QR code on it that can be scanned for the consumer to view the origin of their coffee.
#The image of this QR code would be stored on something like IPFS so it would need a URI.Z

#make input button, enter link once app is up, and auto generate (and display QR code)


#QR Code Code :)
#QRcode functions

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



#Coffee code
st.markdown('# Customer and the supply chain')
image = Image.open('images/coffeeee.jpeg')
st.image(image)

#Streamlit QR code generator inputs and buttons
st.markdown('# QR code Website')
qr_code_content = st.text_input('Enter Streamlit Web App link')
qr_code_filename = st.text_input('QR code "File Name"')

qr_CODE = generate_qrcode(qr_code_content, qr_code_filename)


#Streamlit web app QR code button functions,
button1, button2, button3, button4 = st.columns([1,1,1,1,])

with button1:
    show_qrcode() #show qr code that was generated

with button2: #read qr code button row
    if st.button('Read last QR code'):
        st.write(read_qrcode(file_name=qr_CODE[1])) #read the qr code


##NOT completed:
with button3:
    #Generate QR code
    #info = read_qrcode(file_name=qr_CODE[1])
    #qr_img = qrcode.make(info)  
    

    if st.button('Download'): #NOT WORKING YET
        #imageb = Image.open(qr_CODE[1])
        #b = bytearray(imageb)
        #st.download_button('Download', b, file_name='QR_code')
    
        st.write('error occured')



with button4:
    if st.button('Coffee?'):
        st.balloons()
        st.write('Coffeeeeee!')

#upload file section
#uploaded_file = st.file_uploader("Upload QR Code")

#if uploaded_file is not None:
#not working
#upload, save upload(qr code generator code), reconvert it (read qr code code)
######################################