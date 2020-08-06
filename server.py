import socket

serv = socket.socket()
print("Socket Created")

serv.bind(('localhost', 3456))

serv.listen(1)
print("Waiting for connection")

while True:
    client, addr = serv.accept()
    print("Connected with", addr)

    client.send(bytes('Welcome to my server', 'utf-8'))
    client.close()
