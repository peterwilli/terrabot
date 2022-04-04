from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.core import Coins, Coin

import httpx
import json
import traceback
import math
import sys
import base64

from .exceptions import NonSwapException

class CW20Manager:
    def __init__(self):
        pass
    
    @staticmethod
    def find_swap_contract(config, symbol_from, symbol_to):
        for symbol in config.cw20_tokens:
            token = config.cw20_tokens[symbol]
            if symbol == symbol_to or symbol == symbol_from:
                for swap_symbol in token.swaps:
                    if swap_symbol == symbol_to or swap_symbol == symbol_from:
                        direction = 'buy' if symbol == symbol_to else 'sell'
                        return {
                            'direction': direction,
                            'token_contract_hash': token.contract_hash,
                            'swap_contract_hash': token.swaps[swap_symbol].contract_hash,
                        }
        return None
    
    @staticmethod
    def get_swap_message(config, my_address, symbol_from, symbol_to, offer: float):
        swap_contract_result = CW20Manager.find_swap_contract(config, symbol_from, symbol_to)
        if swap_contract_result is None:
            raise NonSwapException(f"No available swap for {symbol_from}-{symbol_to}!")
        direction = swap_contract_result['direction']
        # Create the message
        if direction == 'buy':
            coin = Coin.parse(f"{math.floor(offer * 1e6)}{symbol_from}").to_data()
            coins = Coins.from_data([coin])
            return MsgExecuteContract(
                sender = my_address,
                contract = swap_contract_result['swap_contract_hash'],
                execute_msg={
                    "swap": {
                        "offer_asset": {
                            "max_spread":"0.005",
                            "info": {"native_token": {"denom": symbol_from}},
                            "amount": str(math.floor(offer * 1e6)),
                        },
                    }
                },
                coins=coins,
            )
        elif direction == 'sell':
            coin = Coin.parse(f"{math.floor(offer * 1e6)}{symbol_from}").to_data()
            coins = Coins.from_data([coin])
            swap_msg = {"swap":{"max_spread":"0.01"}}
            encoded_json = base64.b64encode(json.dumps(swap_msg).encode("utf-8")).decode('ascii')
            return MsgExecuteContract(
                sender = my_address,
                contract = swap_contract_result['token_contract_hash'],
                execute_msg={
                  "send": {
                    "msg": encoded_json,
                    "amount": str(math.floor(offer * 1e6)),
                    "contract": swap_contract_result['swap_contract_hash']
                  }
                },
            )
    
    @staticmethod
    async def portfolio(config, my_address):
        result = {}
        async with httpx.AsyncClient() as client:
            for symbol in config.cw20_tokens:
                token = config.cw20_tokens[symbol]
                try:
                    url = f"{config.chain.url}/wasm/contracts/{token.contract_hash}/store"
                    r = await client.get(
                        url,
                        params = {
                            'query_msg': json.dumps({
                                'balance': {
                                    'address': my_address
                                }
                            }
                        )
                    })
                    content = await r.aread()
                    json_content = json.loads(content)
                    balance = float(json_content['result']['balance'])
                    if balance > 0:
                        result[symbol] = balance / 1e6
                except Exception as e:
                    print("Error! (ignored)")
                    traceback.print_exception(*sys.exc_info())
        return result