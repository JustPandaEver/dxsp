import os
from dotenv import load_dotenv
import asyncio
from web3 import Web3
import many_abis as ma

#YOUR VARIABLES
load_dotenv()
#chain ID being used refer to https://chainlist.org/
chain_id = os.getenv("CHAIN_ID", "10")

#your wallet details
wallet_address = os.getenv("WALLET_ADDRESS", "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE")
private_key = os.getenv("PRIVATE_KEY", "0x111111111117dc0aa78b770fa6a738034120c302")

#1 for 1inch and 2 for Uniswap V2
execution_mode = os.getenv("EXECUTION_MODE", "1")

#DATA from MANY_ABIS FOR RPC and EXCHANGE
chain = ma.get_chain_by_id(chain_id=int(chain_id))
network_provider_url = os.getenv("NETWORK_PROVIDER_URL", chain['rpc'][0])
dex_exchange = os.getenv("DEX_EXCHANGE", chain['dex'][0])

#Block explorer API from ETHERSCAN TYPE EXPLORER
block_explorer_api = os.getenv("BLOCK_EXPLORER_API", "1X23Q4ACZ5T3KXG67WIAH7X8C510F1972TM")

#DEX CONNECTIVITY
w3 = Web3(Web3.HTTPProvider(network_provider_url))



from swapportunity import DexSwap

async def main():
	#SWAP HELPER
	dex = DexSwap(w3,chain_id,wallet_address,private_key,execution_mode,dex_exchange,block_explorer_api)

	#INPUT for QUOTE
	quote = await dex.get_quote('wBTC')
	print("quote ", quote)

	#INPUT for a NORMAL SWAP
	# transaction_amount_out = 10
	# asset_out_symbol = "USDT"
	# asset_in_symbol = "ETH"

	#SWAP EXECUTION
	# transaction = dex.get_swap(transaction_amount_out,asset_out_symbol,asset_in_symbol)
	# print("transaction ", transaction)


if __name__ == "__main__":
    asyncio.run(main())