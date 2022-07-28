import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
    #pip install Pillow
from PIL import Image
    #!pip install opencv-python
import cv2
import qrcode

load_dotenv()

#Get contract
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

#Cache and load main contract 
@st.cache(allow_output_mutation=True)

#load contract function
def contract_load():
    #load abi
    with open(Path('../contracts/compiled/coffeeChain.json')) as f: #compiled json file needs to be called contract_abi.json
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

# Title
st.markdown("---")
st.title("Add Batch")
st.markdown("---")

















# QR Code 
# QRcode functions

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
st.subheader('Generate QR code')
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