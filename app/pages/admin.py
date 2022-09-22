import os
import pandas as pd
from web3 import Web3
from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu
from supply_chain import SupplyChainContract
import qrcode
import cv2
from PIL import Image
import time
import webbrowser

# get contract object
contract = st.session_state.contract

# list of addresses on the testnet
addresses = contract.w3_provider.eth.accounts

# option menu to select nodes or batches
container = st.container()
with container:
    selected = option_menu(
        menu_title=None,
        options=[
            "Nodes",
            "Batches",
        ],
        icons=[
            "building",
            "box",
        ],
        orientation="horizontal",
    )

# ----- NODE VIEW -----
if selected == "Nodes":
    node_action = option_menu(
        menu_title="Select a function",
        options=["Add node", "View node info", "Batches owned by node"],
        icons=[
            "building",
            "info",
            "box",
        ],
        orientation="horizontal",
    )

    # ----- ADD NODE -----
    if node_action == "Add node":
        df = pd.DataFrame()

        # Sidebar Input for contract Details
        name = st.text_input("Name of Business")
        address = st.selectbox("Business ETH address", options=addresses)
        node_type = st.selectbox(
            "Business Type",
            options=["primaryProducer", "Storage", "Roaster", "Retailer", "Consumer"],
        )
        latitude = st.number_input("Business Latitude")
        longitude = st.number_input("Business Longitude")

        # button to push data to smart contract.
        if st.button("Add Business"):
            df = df.append(
                {
                    "address": address,
                    "name": name,
                    "node_type": node_type,
                    "lat": latitude,
                    "lon": longitude,
                    "exists": True,
                },
                ignore_index=True,
            )
            st.write(f"Success! {name}'s details have been added to the smart contract")
            st.write(df)
            st.map(df)
            add_hash = contract.add_node(address, name, node_type, latitude, longitude)

    # ----- VIEW NODE -----
    if node_action == "View node info":
        address = st.selectbox("Business ETH address", options=addresses)
        st.write(contract.get_node(address))

    # ----- NODE OWNERSHIP -----
    if node_action == "Batches owned by node":
        address = st.selectbox("Business ETH address", options=addresses)
        batches = st.selectbox(
            "Select a batch", options=contract.all_batches_owned_by(address)
        )

# ----- BATCH VIEW -----
if selected == "Batches":
    batch_action = option_menu(
        menu_title="Select a function",
        options=[
            "Add batch",
            "Approve purchase",
            "Purchase batch",
            "Batch details",
            "Generate QR code",
        ],
        orientation="horizontal",
    )

    # ----- ADD BATCH -----
    if batch_action == "Add batch":
        df = pd.DataFrame()

        # Title
        st.title("Add Batch")
        st.markdown("---")

        # Input Batch Information
        creator_address = st.selectbox("owner address", options=addresses)
        batch_uri = st.text_input("Batch URI")
        value_eth = st.number_input("Enter Batch Value (ETH)")
        batch_state = st.selectbox("Batch ready to be sent?", [True, False])

        # Button to add data to contract
        if st.button("Add Batch"):
            # use addBatch function to add batch to contract
            df = df.append(
                {
                    "creator_address": creator_address,
                    "batch_uri": batch_uri,
                    "value_eth": value_eth,
                    "batch_state": batch_state,
                },
                ignore_index=True,
            )
            batch = contract.add_batch(
                creator_address, batch_uri, value_eth, batch_state
            )
            st.write(df)
            st.write(f"Batch has been created!\n txn hash: {batch}")

    # ----- PURCHASE BATCH -----
    if batch_action == "Purchase batch":
        # Select a batch to transfer and get owner address
        batch_num = st.number_input("Select a batch number", min_value=0)
        owner = contract.get_batch_owner(batch_num)

        # user input address to transfer batch to
        to = st.selectbox("Batch recipient's address", options=addresses)

        # Button to confirm purchase of a batch
        try:
            if st.button("Confirm purchase"):
                sent_batch = contract.transfer_batch(owner, to, batch_num)
                if sent_batch:
                    st.write(f"Batch has been sent\n txn hash: {sent_batch}")
                else:
                    st.write(
                        "The transaction failed, please check your transaction details"
                    )
        except:
            st.write(
                "Batch not available for purchase, owner must first approve purchase"
            )

    # ----- APPROVE PURCHASE -----
    if batch_action == "Approve purchase":
        # variables used in approval
        batch_num = st.number_input(
            "Select a batch number to apporve for purchase", min_value=0
        )
        owner = contract.get_batch_owner(batch_num)
        recipient = st.selectbox("Batch recipient's address", options=addresses)

        # Button to approve a batch for transfer
        try:
            if st.button("Approve purchase of a batch"):
                approval = contract.approve_transfer(owner, recipient, batch_num)
                if approval:
                    st.write(f"Batch has been approved for sending")
        except:
            st.write(
                "Batch not approved for sending, please check details and try again."
            )

    # ----- BATCH DETAILS -----
    if batch_action == "Batch details":
        batch_num = st.number_input("Select a batch number to view", min_value=0)
        batch_owner = contract.get_batch_owner(batch_num)
        batch_value = contract.get_batch_value(batch_num)
        batch_uri = contract.get_batch_URI(batch_num)
        st.write(f"Current owner: {batch_owner}")
        st.write(f"Current value (ETH): {batch_value}")

        # ----- BATCH INFO -----
        if st.button("View information"):
            uri = contract.get_batch_URI(batch_num)
            webbrowser.open_new_tab(uri)

        batch_value = st.number_input("Update value (ETH)", min_value=0)
        if st.button("Update batch value"):
            contract.set_batch_value(batch_value, batch_num)
            st.write("Batch details successfully updated!")

        batch_state = st.selectbox("Change processing state", [True, False])
        if st.button("Update processing state"):
            contract.set_batch_state(batch_state, batch_num)
            st.write("Batch details successfully updated!")

    # ----- QR CODE -----
    if batch_action == "Generate QR code":
        # qr_code_content select box with batch's data
        batch_num = st.number_input("Select a batch number", min_value=0)

        if st.button("Generate QR code"):
            qr_img = qrcode.make(batch_num)
            st_image = Image.open(qr_img)
            st.image(st_image)
