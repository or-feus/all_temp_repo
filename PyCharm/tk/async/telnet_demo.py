import asyncio
from asyncio import StreamReader, StreamWriter


async def send_event(msg: str):
    await asyncio.sleep(1)

async def echo(reader: StreamReader, writer: StreamWriter): #1
    print('New connection.')

    try:
        while data := await reader.readline(): #2
            writer.write(data.upper()) #3
            await writer.drain()

        print('Leaving Connection.')

    except asyncio.CancelledError: #4
        msg = "Connection dropped!"
        print(msg)

        asyncio.create_task(send_event(msg))


async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port) #5
    async with server:
        await server.serve_forever()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bye!")