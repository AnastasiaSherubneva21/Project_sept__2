import socket
import random
import time


class Client:
    def __init__(self, name):
        self.sock = socket.socket()
        self.sock.connect(('localhost', 15222))
        self.name = name
        self.is_alive = 1

    def connection(self, value):
        try:
            if value == 'timeout':
                time.sleep(6)
            comm = value
            self.sock.send(bytes(comm, encoding='utf-8'))
            data = self.sock.recv(1024)
            print(self.name, comm, data.decode('utf-8'))
            if data.decode('utf-8') == 'Close connection':
                print(self.name, 'Close connection by client')
                self.is_alive = 0
        except socket.error:
            print(self.name, 'Ошибка: ', socket.error)
            print(self.name, 'Close connection by error')
            self.is_alive = 0
            self.sock.close()


k = 5

comm_lst = ['hour', 'minutes', 'seconds', 'error_message', 'stop', 'timeout']
client_lst = []
for i in range(k):
    cl_name = 'client_' + str(i+1)
    cl = Client(cl_name)
    client_lst.append(cl)

while True:
    for i in client_lst:
        if i.is_alive == 0:
            client_lst.remove(i)
        else:
            i.connection(random.choice(comm_lst))
    if len(client_lst) == 0:
        break
