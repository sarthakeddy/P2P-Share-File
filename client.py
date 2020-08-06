import socket

client = socket.socket()

client.connect(('localhost', 3456))

print(client.recv(1024).decode())