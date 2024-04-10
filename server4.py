import socket
import threading

class Server:
    def __init__(self, host = '127.0.0.1', port = 55555):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((host, port))
            self.server.listen()
        except socket.error as e:
            print(str(e))

        self.clients = []
        self.nicknames = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message[:2] == 'pm':
                    _, recipient_name, private_msg = message.split(' ', 2)
                    sender_name = self.nicknames[self.clients.index(client)]
                    if recipient_name in self.nicknames:
                        index = self.nicknames.index(recipient_name)
                        self.clients[index].send(f'Private message from {sender_name}: {private_msg}'.encode('ascii'))
                    else:
                        client.send(f'Error: User {nickname} does not exist!'.encode('ascii'))
                elif message == 'DISCONNECT':
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
                    nickname = self.nicknames[index]
                    self.nicknames.remove(nickname)
                    break
                else:
                    self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f"Nickname of the client is {nickname}!")
            self.broadcast(f"{nickname} joined the chat!".encode('ascii'))
            client.send('Connected to the server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

server = Server()
server.receive()