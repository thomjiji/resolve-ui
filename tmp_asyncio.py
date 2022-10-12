import asyncio

async def main():
    print('Hello ...')
    await asyncio.sleep(2)
    print('... World!')

asyncio.run(main())