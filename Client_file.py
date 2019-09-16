import socket


class Client:
    def __init__(self):
        self.sock = socket.socket()

    def connection(self):
        self.sock.connect(('localhost', 15222))
        while True:
            try:
                comm = input('Введите команду (hour, minutes, seconds, stop): ')
                self.sock.send(bytes(comm, encoding='utf-8'))
                data = self.sock.recv(1024)
                print(data.decode('utf-8'))
                if data.decode('utf-8') == 'Close connection':
                    break
            except socket.error:
                print('Ошибка: ', socket.error)
                break
        self.sock.close()


client = Client()
client.connection()