from multiprocessing.sharedctypes import Value
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st
from supply_chain import SupplyChainContract

#Holds data for all transactions
data = []

# load environment variables
load_dotenv()
w3_providerURI = os.getenv("WEB3_PROVIDER_URI")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
user_address = os.getenv("CONTRACT_USER_ADDRESS")
path_to_contract = './contracts/compiled/coffeeChain.json'

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






#st.write(data)


st.markdown("# Primary Producers")
st.markdown(f"### This batch of coffee was grown in {data[0][0]}")
###### CODE FOR MAPBOX ######
lat = float(data[0][2])
lon = float(data[0][3])


df = pd.DataFrame(
     [[lat, lon]],
     columns=['lat', 'lon'])

st.map(df)
###### --------------- ######


#Code for weather
import json
import requests


openweathermapAPIkey = '81ce3bed1b072f9c171d40c713d5dbed'
response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,daily&units=metric&appid={openweathermapAPIkey}")
weatherData = json.loads(response.text)
# st.image(
#             f" http://openweathermap.org/img/wn/{weatherData['current']['weather'][0]['icon']}@2x.png",
#             width=400, # Manually Adjust the width of the image as per requirement
#         )

#st.markdown("![Image]( http://openweathermap.org/img/wn/{weatherData['current']['weather'][0]['icon']}@2x.png?raw=true)")
st.markdown(f" ![Alt Text](http://openweathermap.org/img/wn/{weatherData['current']['weather'][0]['icon']}@2x.png)")


if weatherData['current']['weather'][0]['icon'] == '01d' or weatherData['current']['weather'][0]['icon'] == '01n':
     st.markdown(f"### ☀️ Weather at {data[0][0]}")
elif weatherData['current']['weather'][0]['icon'] == '02d' or weatherData['current']['weather'][0]['icon'] == '02n':
     st.markdown(f"### 🌤 Weather at {data[0][0]}")
elif weatherData['current']['weather'][0]['icon'] == '03d' or weatherData['current']['weather'][0]['icon'] == '03n':
     st.markdown(f"### ☁️ Weather at {data[0][0]}")
elif weatherData['current']['weather'][0]['icon'] == '04d' or weatherData['current']['weather'][0]['icon'] == '04n':
     st.markdown(f"### ☁️ Weather at {data[0][0]}")
elif weatherData['current']['weather'][0]['icon'] == '09d' or weatherData['current']['weather'][0]['icon'] == '09n':
     st.markdown(f"### 🌧 Weather at {data[0][0]}")
elif weatherData['current']['weather'][0]['icon'] == '10d' or weatherData['current']['weather'][0]['icon'] == '10n':
     st.markdown(f"### 🌦 Weather at {data[0][0]}")
elif weatherData['current']['weather'][0]['icon'] == '11d' or weatherData['current']['weather'][0]['icon'] == '11n':
     st.markdown(f"### ⛈ Weather at {data[0][0]}")
elif weatherData['current']['weather'][0]['icon'] == '13d' or weatherData['current']['weather'][0]['icon'] == '13n':
     st.markdown(f"### 🌨 Weather at {data[0][0]}")
elif weatherData['current']['weather'][0]['icon'] == '50d' or weatherData['current']['weather'][0]['icon'] == '50n':
     st.markdown(f"### 🌫 Weather at {data[0][0]}")

st.markdown(f"The local area has a current temperature of {weatherData['current']['temp']} degrees Celsius with a humidity of {weatherData['current']['humidity']} and a dew point of {weatherData['current']['dew_point']}. Right now there are {weatherData['current']['weather'][0]['description']} with an atmospheric pressure of {weatherData['current']['pressure']} and wind speeds reaching up to {weatherData['current']['wind_speed']} km/h")

st.markdown("### Optimal Coffee Bean Climate")
st.markdown("""Optimal coffee-growing conditions include cool to warm tropical climates, rich soils, and few pests or diseases. 
The world’s Coffee Belt spans the globe along the equator, with cultivation in North, Central, and South America; the Caribbean; Africa; 
the Middle East; and Asia. Brazil is now the world’s largest coffee-producing country. Arabica coffee’s optimal temperature range is 64°–70°F (18°C–21°C). It can tolerate mean annual temperatures up to roughly 73°F (24°C).""")