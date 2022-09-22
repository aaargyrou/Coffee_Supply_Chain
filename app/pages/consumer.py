# UI/web packages
import webbrowser
import streamlit as st
from streamlit_option_menu import option_menu
import requests
from web3 import Web3
import leafmap.foliumap as leafmap

# backend/data structures
import pandas as pd
import json
from supply_chain import SupplyChainContract

# get contract object
contract = st.session_state.contract

# selection bar for users
selected = option_menu(
    menu_title=None,
    options=["Map", "Info", "Growing conditions"],
    icons=["geo-alt", "info", "moisture"],
    orientation="horizontal",
)

# variables for viewing batch info
batch_num = st.number_input("Which batch would you like to track?", min_value=0)

if selected == "Map":
    map = leafmap.Map(center=[-37.8136, 144.9631], zoom=7)
    geojson = contract.batch_geoJSON(batch_num)
    map_data = contract.map_data(batch_num)
    map.add_geojson(geojson, layer_name="supply lines")
    map.add_points_from_xy(
        map_data, x="longitude", y="latitude", color_column="category"
    )
    map.to_streamlit(height=700)


if selected == "Info":
    if st.button("open information for the batch in a new tab"):
        uri = contract.get_batch_URI(batch_num)
        webbrowser.open_new_tab(uri)

    addresses = contract.get_transfer_addresses(batch_num)
    for address in addresses:
        node_from = contract.get_node(address[0])
        node_to = contract.get_node(address[1])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(node_from)
        with col2:
            st.markdown("# -->")
        with col3:
            st.write(node_to)

if selected == "Growing conditions":
    source_coords = contract.get_all_cooordinates(batch_num)[0]
    lat = source_coords[0]
    lon = source_coords[1]

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,daily&units=metric&appid={openweathermapAPIkey}"
    )
    weatherData = json.loads(response.text)

    st.markdown(
        f" ![Alt Text](http://openweathermap.org/img/wn/{weatherData['current']['weather'][0]['icon']}@2x.png)"
    )
    if (
        weatherData["current"]["weather"][0]["icon"] == "01d"
        or weatherData["current"]["weather"][0]["icon"] == "01n"
    ):
        st.markdown(f"### ☀️ Weather at {source_coords}")
    elif (
        weatherData["current"]["weather"][0]["icon"] == "02d"
        or weatherData["current"]["weather"][0]["icon"] == "02n"
    ):
        st.markdown(f"### 🌤 Weather at {source_coords}")
    elif (
        weatherData["current"]["weather"][0]["icon"] == "03d"
        or weatherData["current"]["weather"][0]["icon"] == "03n"
    ):
        st.markdown(f"### ☁️ Weather at {source_coords}")
    elif (
        weatherData["current"]["weather"][0]["icon"] == "04d"
        or weatherData["current"]["weather"][0]["icon"] == "04n"
    ):
        st.markdown(f"### ☁️ Weather at {source_coords}")
    elif (
        weatherData["current"]["weather"][0]["icon"] == "09d"
        or weatherData["current"]["weather"][0]["icon"] == "09n"
    ):
        st.markdown(f"### 🌧 Weather at {source_coords}")
    elif (
        weatherData["current"]["weather"][0]["icon"] == "10d"
        or weatherData["current"]["weather"][0]["icon"] == "10n"
    ):
        st.markdown(f"### 🌦 Weather at {source_coords}")
    elif (
        weatherData["current"]["weather"][0]["icon"] == "11d"
        or weatherData["current"]["weather"][0]["icon"] == "11n"
    ):
        st.markdown(f"### ⛈ Weather at {source_coords}")
    elif (
        weatherData["current"]["weather"][0]["icon"] == "13d"
        or weatherData["current"]["weather"][0]["icon"] == "13n"
    ):
        st.markdown(f"### 🌨 Weather at {source_coords}")
    elif (
        weatherData["current"]["weather"][0]["icon"] == "50d"
        or weatherData["current"]["weather"][0]["icon"] == "50n"
    ):
        st.markdown(f"### 🌫 Weather at {source_coords}")

    st.markdown(
        f"The source growing conditions have a current temperature of {weatherData['current']['temp']} degrees Celsius with a humidity of {weatherData['current']['humidity']} and a dew point of {weatherData['current']['dew_point']}. Right now there are {weatherData['current']['weather'][0]['description']} with an atmospheric pressure of {weatherData['current']['pressure']} and wind speeds reaching up to {weatherData['current']['wind_speed']} km/h"
    )

    st.markdown("### Optimal Coffee Bean Climate")
    st.markdown(
        """Optimal coffee-growing conditions include cool to warm tropical climates, rich soils, and few pests or diseases. 
    The world’s Coffee Belt spans the globe along the equator, with cultivation in North, Central, and South America; the Caribbean; Africa; 
    the Middle East; and Asia. Brazil is now the world’s largest coffee-producing country. Arabica coffee’s optimal temperature range is 64°–70°F (18°C–21°C). It can tolerate mean annual temperatures up to roughly 73°F (24°C)."""
    )
