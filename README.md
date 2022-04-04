# Terrabot - Easily swap (non-)native tokens on the Terra blockchain!

**Warning:** Alpha release!

This Python-package exposes an easy-to-use, high-level API for swaps on the Terra-blockchain.

Whether you're swapping USD for LUNA or mTSLA or any other CW20 token, this library will automatically find and execute the right contracts transparently. All you have to do is supply a configuration for the designated network (currently, only Testnet is supported) and execute swaps using the `swap` function.

## Terrabot is designed for...

- Bots and strategies to be built on top of Terrabot.
- People who just want to automate swaps for their dapps in Python without having to deal with a low-level API. 

## Example

```py
async def main():
    # default_configuration gives us a good starting-point for the respective network
    # this configuration has common tokens and swaps pre-intsalled, suitable for most users
    config = terrabot.default_configuration('testnet')
    client = terrabot.Client(MnemonicKey(mnemonic='test wallet change the seed'), config)
    # Get all available tokens in said network
    tokens = await client.available_tokens()
    # Swap 1 luna for usd
    swap = await client.swap('uluna', 'uusd', 1)
    # Using 10 USD to buy mTSLA, note how you can use the same function
    swap = await client.swap('uusd', 'mTSLA', 10)

asyncio.get_event_loop().run_until_complete(main())
```