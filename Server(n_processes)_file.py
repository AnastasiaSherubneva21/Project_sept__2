import socket
from time import ctime, time
from multiprocessing import freeze_support
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor


class Server:

    def __init__(self, n, m):
        self.sock = socket.socket()
        self.n = n
        self.m = m

    def running(self):
        self.sock.bind(('', 15222))
        self.sock.listen(socket.SOMAXCONN)
        conn, addr = self.sock.accept()
        conn.settimeout(20)
        while True:
            try:
                with ProcessPoolExecutor(max_workers=self.n) as executor:
                    executor.map(self.cycle, [conn])
            except socket.timeout:
                print('Close connection by timeout error')
                break
            except socket.error:
                print('Ошибка: ', socket.error)
                break
        conn.close()

    def cycle(self, conn):
        with ThreadPoolExecutor(max_workers=self.m) as executor:
            data = conn.recv(1024)
            data_l = [data]
            value = [executor.submit(self.return_value, data) for data in data_l]
            for future in as_completed(value):
                value = future.result()
            cort = (conn, value)
            executor.submit(self.send_answer, cort)
            if value == 'Close connection':
                conn.close()
                '''a = 1/0
                print(a)
                print('.')'''


    def return_value(self, comm):
        comm = comm.decode('utf-8')
        str_datetime = str(ctime(time()))
        lst_time = str_datetime.split()
        str_time = lst_time[3]
        if comm == 'hour':
            return int(str_time[0:2])
        elif comm == 'minutes':
            return int(str_time[3:5])
        elif comm == 'seconds':
            return int(str_time[6:])
        elif comm == 'stop':
            return 'Close connection'
        else:
            return 'ERROR'

    def send_answer(self, cort):
        conn = cort[0]
        answer = cort[1]
        conn.send(bytes(str(answer), encoding='utf-8'))


if __name__ == '__main__':
    freeze_support()
    serv = Server(5, 5)
    serv.running()