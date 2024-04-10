import socket
import threading

class Client:
    def __init__(self, nickname, host = '127.0.0.1', port = 55555):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port))
        except socket.error as e:
            print(str(e))
        print("You can write messages now, write quit to exit chat.")
        self.nickname = nickname

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    print(message)
            except socket.error as e:
                print("An error occured: " + str(e))
                self.client.close()
                break

    def write(self):
        while True:
            try:
                message = input("")
                if message == 'quit':
                    self.client.send('DISCONNECT'.encode('ascii'))
                    break
                elif message[:2] == 'pm':
                    message = f'pm {self.nickname}: {message}'
                    self.client.send(message.encode('ascii'))
                else:
                    message = f'{self.nickname}: {message}'
                    self.client.send(message.encode('ascii'))
            except socket.error as e:
                print("An error ocurred: " + str(e))
                self.client.close()
                break

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

nickname = input("Choose your nickname: ")
client = Client(nickname)
client.start()
