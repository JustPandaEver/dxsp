"""
OneInch 🦄
"""
from dxsp.config import settings
from dxsp.main import DexSwap

#https://github.com/mraniki/dxsp/issues/189 

class DexSwapOneInch(DexSwap):
    async def get_quote(
        self,
        asset_in_address,
        asset_out_address,
        amount=1
    ):
        try:
            #pass
            asset_out_amount = self.w3.to_wei(amount, 'ether')
            quote_url = (
                settings.dex_1inch_url
                + str(self.chain_id)
                + "/quote?fromTokenAddress="
                + str(asset_in_address)
                + "&toTokenAddress="
                + str(asset_out_address)
                + "&amount="
                + str(asset_out_amount))
            quote_response = await self._get(
                url=quote_url,
                params=None,
                headers=settings.headers)
            self.logger.debug("quote_response %s", quote_response)
            if quote_response:
                quote_amount = quote_response['toTokenAmount']
                self.logger.debug("quote_amount %s", quote_amount)
                # quote_decimals = quote_response['fromToken']['decimals']
                quote = self.w3.from_wei(int(quote_amount), 'ether')
                # /(10 ** quote_decimals))
                return round(quote, 2)
        except Exception as error:
            raise ValueError(f"Approval failed {error}") 

    async def get_approve(self, token_address):
        # pass
        try:
            approval_check_URL = (
                settings.dex_1inch_url
                + str(self.chain_id)
                + "/approve/allowance?tokenAddress="
                + str(asset_out_address)
                + "&walletAddress="
                + str(self.wallet_address))
            approval_response = await self._get(
                url=approval_check_URL,
                params=None,
                headers=settings.headers)
            approval_check = approval_response['allowance']
            if (approval_check == 0):
                approval_URL = (
                    settings.dex_1inch_url
                    + str(self.chain_id)
                    + "/approve/transaction?tokenAddress="
                    + str(asset_out_address))
                approval_response = await self._get(approval_URL)
                return approval_response
        except Exception as error:
            raise ValueError(f"Approval failed {error}") 



    async def get_swap(self, asset_out_address, asset_in_address, amount):

        try:
            swap_url = (
                settings.dex_1inch_url
                + str(self.chain_id)
                + "/swap?fromTokenAddress="
                + asset_out_address
                + "&toTokenAddress="
                + asset_in_address
                + "&amount="
                + amount
                + "&fromAddress="
                + self.wallet_address
                + "&slippage="
                + settings.dex_trading_slippage
                )
            swap_order = await self._get(
                url=swap_url,
                params=None,
                headers=settings.headers
                )
            swap_order_status = swap_order['statusCode']
            if swap_order_status != 200:
                return
            return swap_order
        except Exception as error:
            raise ValueError(f"Swap failed {error}") 
