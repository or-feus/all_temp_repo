import asyncio
import time
from asyncio import gather


async def async_delay_2():
    delay = 0
    while delay < 1000:
        await asyncio.sleep(0.2)
        print(f"async: {delay} |-> I'm async_delay_2")
        delay += 1


async def async_delay_3():
    delay = 0
    while delay < 1000:
        await asyncio.sleep(0.3)
        print(f"async: {delay} |-> I'm async_delay_3")
        delay += 1


def sync_delay_3():
    delay = 0

    while delay < 1000:
        time.sleep(0.3)
        print(f"sync: {delay} |-> I'm sync_delay_3")
        delay += 1


def main():
    loop = asyncio.get_event_loop()

    loop.run_in_executor(None, sync_delay_3)

    group = gather(*[async_delay_3(), async_delay_2()], return_exceptions=True)

    loop.run_until_complete(group)

    loop.close()


main()
