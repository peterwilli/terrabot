from terra_sdk.key.mnemonic import MnemonicKey
import asyncio
import logging
import json
import terrabot
import yaml

if __name__ == "__main__":
    async def main():
        logging.basicConfig(level=logging.DEBUG)
        config = terrabot.default_configuration('testnet')
        client = terrabot.Client(MnemonicKey(mnemonic='EmeraldsAreCool2'), config)
        print("Test swap LUNA to USD!")
        swap = await client.swap('luna', 'usd', 1)
        await asyncio.sleep(5)
        print("Test swap USD to mTSLA!")
        swap = await client.swap('usd', 'mTSLA', 10)
        await asyncio.sleep(15)
        portfolio = await client.portfolio()
        print("Test swap mTSLA to USD and using USD as fees!")
        swap = await client.swap('mTSLA', 'usd', portfolio['mTSLA'], pay_fees_in = 'usd')
        await asyncio.sleep(5)
        portfolio = await client.portfolio()
        print("Test swap USD to LUNA!")
        swap = await client.swap('usd', 'luna', portfolio['usd'])
    asyncio.get_event_loop().run_until_complete(main())