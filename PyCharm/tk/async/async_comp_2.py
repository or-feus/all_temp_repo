import asyncio


async def f(x): #1
    await asyncio.sleep(0.1)
    return x + 100


async def factory(n): #2
    for x in range(n):
        await asyncio.sleep(0.1)
        yield f, x #3


async def main():
    results = [await f(x) async for f, x in factory(3)] #4
    print(f"results = {results}")


asyncio.run(main())

print()