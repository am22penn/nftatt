from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/cc4226c987ca469fa8130f4c06b16246" #YOU WILL NEED TO TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)

contract = web3.eth.contract(address=contract_address, abi=abi)

def get_ape_info(apeID):
  assert isinstance(apeID,int), f"{apeID} is not an int"
  assert 1 <= apeID, f"{apeID} must be at least 1"

  data = {'owner': "", 'image': "", 'eyes': "" }
	
  #YOUR CODE HERE	
  
  
  try:
    
    #owner
    #Get ape owner by calling contract's `ownerOf` function
    owner = contract.functions.ownerOf(apeID).call()
    data['owner'] = owner

    #image
    #Get ape's metadata location using contract's `tokenURI` function
    tokenURI = contract.functions.tokenURI(apeID).call()
    #Convert to standard IPFS URL if  needed
    if tokenURI.startswith('ipfs://'):
      ipfs_path = tokenURI[7:]
    else:
      ipfs_path = tokenURI
    metadata_url = 'https://ipfs.io/ipfs/' + ipfs_path
    
    #Get metadata JSON from the IPFS URL
    response = requests.get(metadata_url)
    response.raise_for_status()
    metadata_json = response.json()
    #Get image URL from metadata
    image = metadata_json.get('image', '')
    data['image'] = image

    #eyes
    #Get attributes from metadata, looking for eyes trait_type
    attributes = metadata_json.get('attributes', [])
    eyes = ''
    for attr in attributes:
      if attr.get('trait_type') == 'Eyes':
        eyes = attr.get('value', '')
        break
    data['eyes'] = eyes
  except Exception as e:
    print(f"Error processing apeID {apeID}: {e}")

  assert isinstance(data,dict), f'get_ape_info{apeID} should return a dict' 
  assert all( [a in data.keys() for a in ['owner','image','eyes']] ), f"return value should include the keys 'owner','image' and 'eyes'"
  return data

