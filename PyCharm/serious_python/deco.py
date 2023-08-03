import select
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setblocking(0)

server.bind(('localhost', 10000))
server.listen(8)


while True:
    inputs, outputs, excepts = select.select([server], [], [server])

    if server in inputs:
        connection, client_address = server.accept()
        connection.send("hello!\n")

