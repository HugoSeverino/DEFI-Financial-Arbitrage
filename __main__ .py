
from web3 import Web3
import os
from dotenv import load_dotenv
from Functions.Events import Fetch_EventsPairV3,Fetch_EventsPairV2
from Functions.JSON import JsonFile_Data_ListePools

# Load secret .env file
load_dotenv()

# Store credentials
API_Keys = os.getenv('Infura_API')

infura = f'https://mainnet.infura.io/v3/{API_Keys}' #Infura API

#infura = 'http://localhost:8545' #ETH Local Node


 


##################################################################
############## Building Json files of DEX pools ##################
##################################################################

web3 = Web3(Web3.HTTPProvider(infura)) # Creating Web3 instance

UniswapV3_factory =  Web3.toChecksumAddress("0x1f98431c8ad98523631ae4a59f267346ea31f984")
SushiswapV3_factory =  Web3.toChecksumAddress("0xbACEB8eC6b9355Dfc0269C18bac9d6E2Bdc29C4F")
SushiswapV2_factory =  Web3.toChecksumAddress("0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac")
UniswapV2_factory =  Web3.toChecksumAddress("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f")

Fetch_EventsPairV3(web3,UniswapV3_factory,"Uniswap").IterateOverBlocks() #Writing Json List Of pairs
Fetch_EventsPairV3(web3,SushiswapV3_factory,"Sushiswap").IterateOverBlocks() #Writing Json List Of pairs
Fetch_EventsPairV2(web3,SushiswapV2_factory,"Sushiswap").IterateOverBlocks()
Fetch_EventsPairV2(web3,UniswapV2_factory,"Uniswap").IterateOverBlocks()




##################################################################
############## Insert RAW datas in SQL Database ##################
##################################################################


Uniswapv3_Pools = JsonFile_Data_ListePools.ReturnJsonAsPythonReadable("JSON/UniswapV3.json")
print(len(Uniswapv3_Pools))
#for pools in Uniswapv3_Pools:
    #print(pools)




