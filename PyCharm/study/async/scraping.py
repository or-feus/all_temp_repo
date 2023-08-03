from bs4 import BeautifulSoup
import aiohttp
import asyncio


async def fetch(session, url):
    headers = {
        "X-Naver-Client-Id": "Jez9TwwuymLjvnH7T4b2",
        "X-Naver-Client-Secret": "g0nOdE4wO6"
    }
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]

        print(images)

async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"
    urls = [f"{BASE_URL}?query={keyword}&display=20&start={1+i*20}" for i in range(10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == '__main__':
    asyncio.run(main())
