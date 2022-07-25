#to do - Sidebar - keanu
#Page Navigation?
#URI for the coffee package? 
#Buttons to call contract functions
#User input to contract

#IMPORTS
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

#Side BAR
#code here

###Get contract

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

#Cache and load main contract 
@st.cache(allow_output_mutation=True)

#load contract function
def contract_load():
    #load abi
    with open(Path('compiled_abi/contract_abi.json')) as f: #compiled json file needs to be called contract_abi.json
        contract_abi = json.load(f)

    #Get contract address 
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    
    #Geting contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    return contract

#Load the contract
contract = contract_load()

#Contract Inputs

#select accounts method, dropdown select account
#accounts = w3.eth.accounts
#account = accounts[0]
#user = st.selectbox("Select Account", options=accounts)

#Token details
coffee_bag_token_id = st.number_input("Enter a Bag Token ID to display", value=0, step=1)
if st.button("Display Bag Token ID"):
    # Get the last location
    current_location = contract.functions.ownerOf(coffee_bag_token_id).call()
    st.write(f"This bag belongs to {current_location}")

    # Get the certificate's metadata, if we have uri?
    #bag_uri = contract.functions.tokenURI(coffee_bag_token_id).call()
    #st.write(f"The Bag's tokenURI metadata is {bag_uri}")




#Buttons to call contract Functions in streamlit

#URI
#coffee packaging would have a QR code on it that can be scanned for the consumer to view the origin of their coffee.
#The image of this QR code would be stored on something like IPFS so it would need a URI.Z

#make input button, enter link once app is up, and auto generate (and display QR code)


#QR Code
#Import QRcode libary
import qrcode

#QRcode function
def generate_qrcode(input_str, file_name):
#Generate QR code
    qr_img = qrcode.make(input_str)  
#Save image file   
    qr_img.save(file_name+'.jpg')
#read QR code - https://www.javatpoint.com/generate-a-qr-code-using-python
#maybe use streamlit download to download qr code

st.markdown('# QR code Website')
qr_code_content = st.text_input('Enter Streamlit Web App link')

