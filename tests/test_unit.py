"""
 DEXSWAP Unit Test
"""

from unittest.mock import patch, MagicMock
import re
import pytest
import requests
from dxsp import DexSwap
from dxsp.config import settings



@pytest.fixture
def dex():
    return DexSwap()


@pytest.fixture
async def settings_fixture():
    """settings"""
    with patch("dxsp.config.settings", autospec=True) as mock_settings:
        mock_settings.dex_wallet_address = "0x1234567890123456789012345678901234567899"
        mock_settings.dex_private_key = "0xdeadbeef"
        yield mock_settings


@pytest.fixture
async def router(dex):
    """router"""
    return await dex.router()


@pytest.fixture
async def quoter(dex):
    """quoter"""
    return await dex.quoter()


@pytest.mark.asyncio
async def test_init_dex():
    """Init Testing"""
    dex = DexSwap()
    check = "DexSwap" in str(type(dex))
    assert check is True
    assert dex.w3 is not None
    assert dex.chain_id is not None
    assert dex.protocol_type is not None
    assert dex.protocol_type == "uniswap_v2"
    assert dex.wallet_address.startswith("0x")
    assert dex.wallet_address == "0x1234567890123456789012345678901234567890"
    assert dex.private_key.startswith("0x")
    assert dex.account == "1 - 34567890"


def test_setting_dex_swap_init():
    with patch("dxsp.config.settings", autospec=True):
        settings.dex_wallet_address = "0x1234567890123456789012345678901234567899"
        settings.dex_private_key = "0xdeadbeet"

        dex = DexSwap()
        assert dex.wallet_address == "0x1234567890123456789012345678901234567899"
        assert dex.private_key == "0xdeadbeet"
        assert dex.account == "1 - 34567899"


def test_chain_dex_swap_init():
    with patch("dxsp.config.settings", autospec=True):
        settings.dex_wallet_address = "0x1234567890123456789012345678901234567899"
        settings.dex_private_key = "0xdeadbeet"
        settings.dex_chain_id = 10

        dex = DexSwap()
        assert dex.wallet_address == "0x1234567890123456789012345678901234567899"
        assert dex.private_key == "0xdeadbeet"
        assert dex.account == "10 - 34567899"
        assert dex.chain_id == 10


@pytest.mark.asyncio
async def test_get(dex):
    result = await dex._get(
        "http://ip.jsontest.com",
        params=None,
        headers=None)
    assert result is not None


@pytest.mark.asyncio
async def test_router(dex):
    router = await dex.router()
    assert router is not None


@pytest.mark.asyncio
async def test_quoter(dex):
    """quoter Testing"""
    quoter = await dex.quoter()
    if quoter:
        assert quoter is not None


@pytest.mark.asyncio
async def test_search_contract(dex):
    address = await dex.search_contract("WBTC")
    assert address.startswith("0x")

    address = await dex.search_contract("USDT")
    assert address is not None
    assert address.startswith("0x")

    address = await dex.search_contract("UNKNOWN")
    assert address is None



@pytest.mark.asyncio
async def test_get_abi(dex, mocker):
    # Mock the _get method to return a mock response
    mock_resp = {"status": "1", "result": "0x0123456789abcdef"}
    mocker.patch.object(dex, "_get", return_value=mock_resp)

    abi = await dex.get_abi("0x1234567890123456789012345678901234567890")

    assert abi == "0x0123456789abcdef"


@pytest.mark.asyncio
async def test_get_noabi_mock(dex):
    abi = await dex.get_abi("0x1234567890123456789012345678901234567890")
    assert abi is None


@pytest.mark.asyncio
async def test_get_token_contract(dex):
    """get_token_contract Testing"""
    contract = await dex.get_token_contract("UNI")
    print(contract)
    print(type(contract))
    print(contract.functions)
    if contract:
        assert contract is not None
        assert type(contract) is not None
        assert contract.functions is not None


@pytest.mark.asyncio
async def test_get_quote(dex):
    """getquote Testing"""
    quote = await dex.get_quote("UNI")
    print(quote)
    if quote:
        assert quote is not None
        assert quote.startswith("🦄")


@pytest.mark.asyncio
async def test_get_quote_error(dex):
    """Test get_quote() method"""
    quote = await dex.get_quote("THISISNOTATOKEN")
    assert quote is None

@pytest.mark.asyncio
async def test_get_quote_uniswap(dex):
    # Call the get_quote_uniswap method and check the result
    quote = await dex.get_quote_uniswap(
        dex.w3.to_checksum_address("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"),
        dex.w3.to_checksum_address("0xdac17f958d2ee523a2206206994597c13d831ec7"),
        1000000000)
    print(f"quote: {quote}")
    assert quote is not None
    assert quote.startswith("🦄")
    expected_quote_pattern = r"🦄 \d+ USDT"
    assert re.match(expected_quote_pattern, quote) is not None


# @pytest.mark.asyncio
# async def test_get_approve_uniswap(dex):
#     with patch("dxsp.config.settings", autospec=True):
#         settings.dex_wallet_address = "0x1234567890123456789012345678901234567899"

#         allowance = await dex.get_approve_uniswap(symbol="USDT")
#         assert allowance is None



@pytest.mark.asyncio
async def test_get_swap_uniswap(dex):
    asset_out_address = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
    asset_in_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    amount = 100

    # Create a mock object for self.get_quote_uniswap()
    get_quote_mock = MagicMock()
    get_quote_mock.return_value = [50]

    # Create a mock object for self.w3.eth.get_block()
    get_block_mock = MagicMock()
    get_block_mock.return_value = {"timestamp": 1000}

    # Set up the test instance
    dex.get_quote_uniswap = get_quote_mock
    dex.w3.eth.get_block = get_block_mock
    dex.wallet_address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    dex.protocol_type = "uniswap_v2"

    # Call the function being tested
    swap_order = await dex.get_swap_uniswap(
        asset_out_address,
        asset_in_address,
        amount)
    print(f"swap_order: {swap_order}")
    # Check the output
    assert swap_order is not None

@pytest.mark.asyncio
async def test_get_0x_quote(dex):
    with patch("dxsp.config.settings", autospec=True):
        settings.dex_wallet_address = "0x1234567890123456789012345678901234567899"
        settings.dex_private_key = "0xdeadbeet"
        settings.dex_chain_id = 1
        settings.dex_rpc = "https://rpc.ankr.com/eth_goerli"
        settings.dex_0x_url = "https://goerli.api.0x.org"
        settings.dex_protocol_type = "0x"
        # Test function ETH > UNI
        result = await dex.get_0x_quote(
            "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
            1)
        assert result is not None
        assert isinstance(result, float)


@pytest.mark.asyncio
async def test_get_0x_quote_fail(dex):
    with patch("dxsp.config.settings", autospec=True):
        settings.dex_wallet_address = "0x1234567890123456789012345678901234567899"
        settings.dex_private_key = "0xdeadbeet"
        settings.dex_chain_id = 1
        settings.dex_rpc = "https://rpc.ankr.com/eth_goerli"
        settings.dex_0x_url = "https://goerli.api.0x.org"
        settings.dex_protocol_type = "0x"
        # Test function DAI > UNI
        result = await dex.get_0x_quote(
            "0xE68104D83e647b7c1C15a91a8D8aAD21a51B3B3E",
            "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
            1)
        assert result is None


# @pytest.mark.asyncio
# async def test_get_approve(dex):
#     result = await dex.get_approve("UNI")
#     print(result)
#     assert result is not None


# @pytest.mark.asyncio
# async def test_get_confirmation(mocker):
#     mock_w3 = mocker.MagicMock()
#     mock_receipt = mocker.MagicMock()
#     mock_block = mocker.MagicMock()

#     mock_w3.eth.get_transaction.return_value = mock_receipt
#     mock_w3.eth.get_block.return_value = mock_block

#     order_hash = "0x1234"

#     mock_receipt.return_value = {
#         "blockNumber": 123,
#         "blockHash": "0x5678",
#         "to": "0x1234567890123456789012345678901234567890",
#         "value": 10,
#         "gas": 1000,
#     }
#     mock_block.return_value = {"timestamp": 1600000000}

#     expected_trade = {
#         "timestamp": 1600000000,
#         "id": "0x5678",
#         "instrument": "0x1234567890123456789012345678901234567890",
#         "contract": "0x1234567890123456789012345678901234567890",
#         "amount": 10,
#         "price": 10,
#         "fee": 1000,
#         "confirmation": (
#             "➕ Size: 10.0\n"
#             "⚫️ Entry: 10.0\n"
#             "ℹ️ 0x5678\n"
#             "🗓️ 1600000000"
#         ),
#     }

#     obj = DexSwap(mock_w3)
#     assert await obj.get_confirmation(order_hash) is not None
#     mock_w3.eth.get_transaction.assert_called_once_with(order_hash)
#     mock_w3.eth.get_block.assert_called_once_with(123)


# @pytest.mark.asyncio
# async def test_execute_order(dex):
#     order_params = {
#         'action': 'BUY',
#         'instrument': 'ETH',
#         'quantity': 1
#     }
#     result = await dex.execute_order(order_params)
#     print(result)
#     assert result.__class__ == ValueError
#     assert str(result) == "No Money"

@pytest.mark.asyncio
async def test_no_money_get_swap(dex):
    swap = await dex.get_swap(
        "WBTC",
        "USDT",
        1)
    print(f"swap: {swap}")
    assert swap is None


@pytest.mark.asyncio
async def test_get_gas(dex):
    # Create a mock transaction
    mock_tx = {"to": "0x1234567890123456789012345678901234567890",
               "value": "1000000000000000000"}

    # Call the get_gas method and check the result
    gas_estimate = await dex.get_gas(mock_tx)
    assert gas_estimate > 1


@pytest.mark.asyncio
async def test_get_gas_price(dex):
    # Call the get_gasPrice method and check the result
    gas_price = await dex.get_gas_price()
    print(f"gas_price: {gas_price}")
    assert gas_price is not None


@pytest.mark.asyncio
async def test_get_account_balance(dex):
    # Call the get_account_balance method and check the result
    balance = await dex.get_account_balance()
    assert balance is not None
    assert balance >= 0


@pytest.mark.asyncio
async def test_get_token_balance(dex):
    # Call the get_token_balance method and check the result
    with patch("dxsp.config.settings", autospec=True) as mock_settings:
        mock_settings.dex_wallet_address = "0x1234567890123456789012345678901234567899"
        mock_settings.dex_private_key = "0xdeadbeef"
    token_balance = await dex.get_token_balance("UNI")
    assert isinstance(token_balance, int)
    assert token_balance >= 0
