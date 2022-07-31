# Coffee_Supply_Chain - DRAFT README.md

## Contents
1. [Overview of the Project](#overview-of-the-project)
2. [Technologies Used](#technologies-used)
3. [Getting Started](#getting-started)
    * [Installing](#installing)
4. [User Interface](#utilising-the-user-interface)


---
## Overview of the Project

This project aims to solve the problem of tracking the full supply chain from the production of coffee beans to the consumer hands.

Utilising a Streamlit front end this supply chain tracks the transactions and movement of coffee beans from:
* Harvester
* Storage
* Roaster
* Retailer
* Consumer

Ultimately allowing the end user (consumer) to scan a QR code enabling them to access the full history of the supply chain of a specific bag of coffee.


![Flow Chart](./Images/flow_structure.png)


## Technologies Used

* [RemixIDE](https://remix-project.org/)
* [Web3](https://web3py.readthedocs.io/en/stable)
* [Streamlit](https://streamlit.io/)
* [Dotenv](https://pypi.org/project/python-dotenv/)
* [Python 3.7]()
* [QR Code](https://pypi.org/project/qrcode/)
* [Ganache](https://trufflesuite.com/ganache/)
* [Metamask](https://metamask.io/)


## Getting Started
### Installing
**A step by step series of examples on how to install this application:**

	git clone https://github.com/aaargyrou/Coffee_Supply_Chain.git

Ensure all technologies have been installed:

    pip install streamlit
    pip install qrcode
    pip install web3
    pip install python-dotenv
    pip install opencv-python
    pip install Pillow
    pip install pathlib
    pip install pandas
    pip install numpy


## Install Ganache
Ganache has been used to test and validate transactions are performing correctly when using the webapp and to provide a local test net with addresses. 
Ganache can be downloaded [here](https://trufflesuite.com/ganache/).

Because this webapp has been tested with hard coded testcases, running the populate_supply_chain function requires a specific ganache workspace. This can be replicated by opening a new workspace, under accounts and keys enter the following Mnemonic: **profit garage machine open enact embody pigeon correct spread tribe improve token**

**Warning: Do not use these addresses for testnet or Mainnet ethereum addresses, this is for testing purposes only.**

The Addresses in the workspace should look as follows:

![ganache_addresses](Images/ganache_screenshot.png)


## Deploying the contract
After connecting a ganache address to metamask, the contract can be deployed on the testnet via remix and injected web3. To do this, [link ganache to metamask](https://dapp-world.com/blogs/01/how-to-connect-ganache-with-metamask-and-deploy-smart-contracts-on-remix-without-1619847868947), and import the contract.sol file into remix and deploy after compiling. If the contract does not deploy, try resetting the account in the metamask settings to get the correct nonce value.

![metamask](Images/contract_deploy.png)


## Environment variables
in order to initilise the SupplyChainContract, the follwoing variables should be present in a .env 
file.

WEB3_PROVIDER_URI="GANACHE_RPC_SERVER_ADDRESS"

SMART_CONTRACT_ADDRESS="ADDRESS_OF_DEPLOYED_SMART_CONTRACT"

CONTRACT_USER_ADDRESS = "ADDRESS_USED_TO_DEPLOY_THE_CONTRACT"
## Utilising the User Interface
**A step by step series of examples on how to use this application:**

Navigate to the folder

    cd Coffee_Supply_Chain

Run the Streamlit Application

    streamlit run app.py

(note: keanu_streamlit_frontend.py file runs on its own, py_extra_codes contains 2 split in half sections (that run independantly) from the 'keanu_streamlit_frontend.py' file, as the code was required for 2 seperate apps. Admin App and Customer App)