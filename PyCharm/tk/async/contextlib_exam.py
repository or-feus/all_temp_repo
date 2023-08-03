from contextlib import contextmanager, asynccontextmanager


@asynccontextmanager #1
async def web_page(url): #2
    data = await download_webpage(url) #3
    yield data #4
    await update_stats(url) #5

async with web_page('google.com') as data: #6
    process(data)
