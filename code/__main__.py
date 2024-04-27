
from web3 import Web3
import os
from dotenv import load_dotenv
from Functions.Events import Fetch_EventsPairV3,Fetch_EventsPairV2
from Functions.JSON import JsonFile_Data_ListePools
from Functions.SQL import SQL_Pools,SQL_Init,SQL_Token



# Load secret .env file
load_dotenv()

# Store credentials
#API_Keys = os.getenv('Infura_API')

API_Keys = os.getenv('Base_API')
#infura = f'https://mainnet.infura.io/v3/{API_Keys}'  # Infura API

#infura = 'http://localhost:8545' #ETH Local Node

infura = f"https://base-mainnet.g.alchemy.com/v2/{API_Keys}"




##################################################################
############## Building Json files of DEX pools ##################
##################################################################

web3 = Web3(Web3.HTTPProvider(infura)) # Creating Web3 instance
#SQL_Token().Update_Error(web3)
UniswapV3_factory =  "0x33128a8fC17869897dcE68Ed026d694621f6FDfD"
SushiswapV3_factory =  "0xc35DADB65012eC5796536bD9864eD8773aBc74C4"
SushiswapV2_factory =  "0x71524B4f93c58fcbF659783284E38825f0622859"
UniswapV2_factory =  "0x8909Dc15e40173Ff4699343b6eB8132c65e18eC6"

Fetch_EventsPairV3(web3,UniswapV3_factory,"Uniswap").IterateOverBlocks() #Writing Json List Of pairs
Fetch_EventsPairV3(web3,SushiswapV3_factory,"Sushiswap").IterateOverBlocks() #Writing Json List Of pairs
Fetch_EventsPairV2(web3,SushiswapV2_factory,"Sushiswap").IterateOverBlocks()
Fetch_EventsPairV2(web3,UniswapV2_factory,"Uniswap").IterateOverBlocks()




##################################################################
############## Insert RAW datas in SQL Database ##################
##################################################################

SQL_Init()  #Creating Database and table if not existing



Uniswapv3_ListPools = JsonFile_Data_ListePools.ReturnJsonAsPythonReadable("JSON/UniswapV3.json")




SQL_Pools().Update_Database(Uniswapv3_ListPools,3)

Sushiswapv3_ListPools = JsonFile_Data_ListePools.ReturnJsonAsPythonReadable("JSON/SushiswapV3.json")



SQL_Pools().Update_Database(Sushiswapv3_ListPools,3)


Uniswapv2_ListPools = JsonFile_Data_ListePools.ReturnJsonAsPythonReadable("JSON/UniswapV2.json")



SQL_Pools().Update_Database(Uniswapv2_ListPools,2)

Sushiswapv2_ListPools = JsonFile_Data_ListePools.ReturnJsonAsPythonReadable("JSON/SushiswapV2.json")



SQL_Pools().Update_Database(Sushiswapv2_ListPools,2)



##################################################################
################# Display Some informations ######################
##################################################################

Number_Of_Pools = SQL_Pools().Count() #Return Number of Pools
Number_Of_Tokens = SQL_Token().Count() #Return Number of Tokens


print(f'We have {Number_Of_Pools} Pools and {Number_Of_Tokens} Token in our Mysql Database')

##################################################################
################# Update Error and Orphelins #####################
##################################################################

#Because we're doing financial arbitrage, we don't need to look for token which appears only one time.

Number_Of_Pools_no_Orphelin = SQL_Pools().Update_Orphelin()
Number_Of_Tokens_no_Orphelin = SQL_Token().Update_Orphelin()


print(f'After excluding orphelins  we have now {Number_Of_Pools_no_Orphelin} Pools and {Number_Of_Tokens_no_Orphelin} Tokens')

SQL_Token().Update_Error(web3) #Update Database to exclude token orphelins

##################################################################
############### Update Pools Reserves and infos ##################
##################################################################

SQL_Pools().Update_Pools_Data(web3)




