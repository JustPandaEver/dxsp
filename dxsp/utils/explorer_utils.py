"""
 DEX SWAP
EXPLORER
"""

from datetime import datetime, timedelta

from dxsp.config import settings
from dxsp.utils.utils import get


async def get_explorer_abi(address):
    if not settings.dex_block_explorer_api:
        return None

    params = {
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": settings.dex_block_explorer_api
    }
    resp = await get(
        url=settings.dex_block_explorer_url, params=params)
    return resp["result"] if resp['status'] == "1" else None

async def get_account_transactions(
    contract_address,
    wallet_address,
    period=24):
    """
    Retrieves the account transactions 
    within a specified time period
    for the main asset activity
    """
    pnl_dict = {"pnl": 0, "tokenList": {}}
    if not settings.dex_block_explorer_api:
        return pnl_dict

    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": contract_address,
        "address": wallet_address,
        "page": "1",
        "offset": "100",
        "startblock": "0",
        "endblock": "99999999",
        "sort": "desc",
        "apikey": settings.dex_block_explorer_api
    }

    response = await get(
        url=settings.dex_block_explorer_url, params=params)

    if response.get('status') == "1" and "result" in response:
        current_time = datetime.utcnow()
        time_history_start = current_time - timedelta(hours=period)

        for entry in response["result"]:
            token_symbol = entry.get("tokenSymbol")
            value = int(entry.get("value", 0))
            timestamp = int(entry.get("timeStamp", 0))
            transaction_time = datetime.utcfromtimestamp(timestamp)

            if transaction_time >= time_history_start and token_symbol:
                pnl_dict["tokenList"][token_symbol] = (
                pnl_dict["tokenList"].get(token_symbol, 0) + value)
                pnl_dict["pnl"] += value

    return pnl_dict