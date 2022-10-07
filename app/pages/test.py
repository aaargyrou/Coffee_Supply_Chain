import os
import pandas as pd
import plotly.express as px
import streamlit as st
import webbrowser
from dotenv import load_dotenv
from supply_chain import SupplyChainContract
import matplotlib.pyplot as plt

contract = st.session_state.contract

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


def test_nodes():
    nodes = pd.read_csv("../tests/test_nodes.csv", index_col="index")

    # Add all data in nodes to the testnet
    for index, node in nodes.iterrows():
        contract.add_node(node[1], node[0], node[4], node[2], node[3])


def test_batches():
    batches = pd.read_csv("../tests/test_batches.csv", index_col="index")
    for index, batch in batches.iterrows():
        contract.add_batch(batch[0], batch[1], batch[2], batch[3])


def test_transactions():
    transactions = pd.read_csv("../tests/test_transactions.csv", index_col="index")
    for index, transaction in transactions.iterrows():
        # due to default false batch state, batch states need to be set to true before transactions occur
        contract.set_batch_state(True, int(transaction[2]))
        contract.set_batch_value(transaction[3], int(transaction[2]))

        # approvals for transfer also need to be set to allow transfer of the NFT
        contract.approve_transfer(transaction[0], transaction[1], int(transaction[2]))
        contract.transfer_batch(transaction[0], transaction[1], int(transaction[2]))


if st.button("Run tests"):
    test_nodes()
    test_batches()
    test_transactions()
    st.balloons()
    st.write("Coffeeeeee!")
