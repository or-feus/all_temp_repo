import asyncio


async def download_page(url):
    # asyncio.sleep(1)
    await asyncio.sleep(1)  # await 키워드 사용
    # html 분석
    print("complete download:", url)


async def main():
    await asyncio.gather(
        download_page("url_1"),
        download_page("url_2"),
        download_page("url_3"),
        download_page("url_4"),
        download_page("url_5")
    )


asyncio.run(main())