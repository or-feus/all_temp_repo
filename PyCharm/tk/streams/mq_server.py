import asyncio
from asyncio import StreamReader, StreamWriter, gather
from collections import defaultdict, deque
from typing import DefaultDict, Deque

from streams.msg_proto import read_msg, send_msg  # 1

SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)  # 2


async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info('peername')  # 3
    subscribe_chan = await read_msg(reader)  # 4
    SUBSCRIBERS[subscribe_chan].append(writer)  # 5
    print(f"Remote {peername} subscribed to {subscribe_chan}")
    try:
        while channel_name := await read_msg(reader):  # 6
            data = await read_msg(reader)  # 7
            print(f"Sending to {channel_name}: {data[:19]}...")
            conns = SUBSCRIBERS[channel_name]  # 8
            if conns and channel_name.startswith(b'/queue'):  # 9
                conns.rotate()  # 10
                conns = [conns[0]]  # 11
            await gather(*[send_msg(c, data) for c in conns])  # 12
    except asyncio.CancelledError:
        print(f"Remote {peername} closing connection.")
        writer.close()
        await writer.wait_closed()
    except asyncio.IncompleteReadError:
        print(f"Remote {peername} disconnected")
    finally:
        print(f"Remote {peername} closed")
        SUBSCRIBERS[subscribe_chan].remove(writer)  # 13


async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()

        try:
            asyncio.run(main(client, host='127.0.0.1', port=25000))

        except KeyboardInterrupt:
            print('Bye!')
