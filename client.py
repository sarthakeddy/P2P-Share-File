import os
import pickle
import threading
import socket
from threading import *


class peerServer:
    def __init__(self):
        print("Welcome to peer to peer file sharing system")
        self.file_name = ""
        self.peer_port = 0

    def start_server(self):
        while True:
            choice = input("Menu \n(1) Register\n(2) Search\n(3) List all files\n(4) Download\n(5) Exit server\n")
            choice = int(choice)
            if choice == 1:
                peer_id = input("Enter the 4 digit peer id: ")
                self.file_name = input("Enter file name: ")
                self.peer_port = int(peer_id)
                self.register()
                # start_listener(self.peer_port, 'loaclhost')

            elif choice == 2:
                self.search()

            elif choice == 3:
                self.list_all()

            elif choice == 4:
                peer_id = input("Enter the 4 digit peer id: ")
                file_name = input("Enter file name: ")
                self.download(int(peer_id), file_name)

            elif choice == 5:
                break

            else:
                continue

    def register(self):
        client = socket.socket()
        client.connect(('localhost', 3456))
        register_data = [1, self.peer_port, self.file_name]
        data = pickle.dumps(register_data)
        client.send(data)
        state = client.recv(1024)
        print(state.decode('utf-8'))
        client.close()

    def search(self):
        client = socket.socket()
        client.connect(('localhost', 3456))
        file_name = input("Enter file name: ")
        register_data = [2, file_name]
        data = pickle.dumps(register_data)
        client.send(data)
        state = pickle.loads(client.recv(1024))
        self.print_list(state[0], state[1])
        client.close()

    def list_all(self):
        client = socket.socket()
        client.connect(('localhost', 3456))
        data = pickle.dumps(str(3))
        client.send(data)
        state = pickle.loads(client.recv(1024))
        self.print_list(state[0], state[1])
        client.close()

    def print_list(self, files, keys):
        if len(files) == 0:
            print("There is no file available")
        else:
            print("Peer ID  File Name    Date Added")
            for item in files:
                print(item[keys[0]],"  ",item[keys[1]], "    ", item[keys[2]])

    def download(self, peer_id, file_name):
        client = socket.socket()
        client.connect(('localhost', 3456))
        list_data = [4, str(file_name)]
        data = pickle.dumps(list_data)
        client.send(data)

        file_path = os.path.join(os.getcwd(), '..')
        file_path = os.path.join(file_path, 'SharingFiles')
        file_path = os.path.join(file_path, 'downloads')

        with open(os.path.join(file_path, file_name), 'wb') as myfile:
            while True:
                data = client.recv(1024)
                if not data:
                    myfile.close()
                    break
                myfile.write(data)
        client.close()
        print('File is downloaded successfully.')


peer = peerServer()
peer.start_server()