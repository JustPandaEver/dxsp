"""
0️⃣x
"""
from dxsp.config import settings
from dxsp.main import DexSwap

class DexSwapZeroX(DexSwap):
    async def get_quote(self, buy_address, sell_address, amount=1):
        #pass
        try:
            out_amount = amount * (10 ** await self.get_token_decimals(buy_address)) ##1000000000
            url = f"{settings.dex_0x_url}/swap/v1/quote?buyToken={str(sell_address)}&sellToken={str(buy_address)}&buyAmount={str(out_amount)}"
            headers = {"0x-api-key": settings.dex_0x_api_key}
            response = await self.get(url, params=None, headers=headers)
            print(response)
            if response:
                raw_amount = round(float(response['guaranteedPrice']), 6)
        except Exception as error:
            raise ValueError(f"Quote failed {error}") 


    async def get_swap(self, buy_address, sell_address, amount):
        swap_order = await self.get_quote(buy_address, sell_address, amount)
        return await self.get_sign(swap_order)