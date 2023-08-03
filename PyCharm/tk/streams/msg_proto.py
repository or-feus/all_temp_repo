from asyncio import StreamReader, StreamWriter


async def read_msg(stream: StreamReader) -> bytes:
    size_bytes = await stream.readexactly(4) #1
    size = int.from_bytes(size_bytes, byteorder='big') #2
    data = await stream.readexactly(size) #3
    return data

async def send_msg(stream: StreamWriter, data: bytes):
    size_bytes = len(data).to_bytes(4, byteorder='big')
    stream.writelines([size_bytes, data]) #4
    await stream.drain()