import asyncio
import math
from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from terra_sdk.client.lcd import AsyncLCDClient
from terra_sdk.core import Coins, Coin
from terra_sdk.core.market import MsgSwap
from box import Box
from terrabot.cw20_manager import CW20Manager
import logging

class Client:
    def __init__(self, key, config):
        self.config = Box(config)
        self.terra = AsyncLCDClient(chain_id=self.config.chain.id, url=self.config.chain.url)
        self.wallet = self.terra.wallet(key)
        logging.debug(f"My address: {self.wallet.key.acc_address}")
        
    async def available_tokens(self):
        total_supply = await self.terra.bank.total()
        total_supply = [d.denom[1:] for d in total_supply[0]]
        return total_supply
        
    async def portfolio(self):
        balance_native = await self.terra.bank.balance(self.wallet.key.acc_address)
        balance_native = {b.denom[1:]: b.amount / 1e6 for b in balance_native[0]}
        
        balance_cw20 = await CW20Manager.portfolio(self.config, self.wallet.key.acc_address)
        balance_native.update(balance_cw20)
        return balance_native
        
    async def swap(self, symbol_from, symbol_to, offer: float, message: str = None, pay_fees_in: str = "luna"):
        available_tokens = await self.available_tokens()
        def create_tx_options(msgs):
            if pay_fees_in == "luna":
                return CreateTxOptions(
                    msgs=msgs,
                    gas_prices="0.15uluna",
                    gas_adjustment=1.4,
                    fee_denoms=["uluna"],
                    memo=message
                )
            else:
                return CreateTxOptions(
                    msgs=msgs,
                    fee_denoms=[f"u{pay_fees_in}"],
                    memo=message
                )
        if symbol_from in available_tokens and symbol_to in available_tokens:
            # Native swap
            msg = MsgSwap(
                trader = self.wallet.key.acc_address,
                offer_coin = Coin.parse(f"{math.floor(offer * 1e6)}u{symbol_from}"),
                ask_denom = f"u{symbol_to}",
            )
            tx = await self.wallet.create_and_sign_tx(create_tx_options([msg]))
            await self.terra.tx.broadcast(tx)
        else:
            swap_message = CW20Manager.get_swap_message(self.config, self.wallet.key.acc_address, symbol_from, symbol_to, offer)
            logging.debug("Non-native swap: " + str(swap_message))
            tx = await self.wallet.create_and_sign_tx(create_tx_options([swap_message]))
            await self.terra.tx.broadcast(tx)