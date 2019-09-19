import socket
from time import ctime, time
from multiprocessing import freeze_support
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor


class Server:

    def __init__(self, n):
        self.sock = socket.socket()
        self.n = n

    def running(self):
        self.sock.bind(('', 15222))
        self.sock.listen(socket.SOMAXCONN)
        with ProcessPoolExecutor(max_workers=self.n) as executor:
            while True:
                conn = 1
                executor.map(self.worker, [conn])

    def worker(self, conn):
        conn, addr = self.sock.accept()
        conn.settimeout(5)
        with ThreadPoolExecutor() as executor:
            with conn:
                while True:
                    try:
                        data = conn.recv(1024)
                        data_l = [data]
                        value = [executor.submit(self.return_value, data) for data in data_l]
                        for future in as_completed(value):
                            value = future.result()
                        cort = (conn, value)
                        executor.submit(self.send_answer, cort)
                        if value == 'Close connection':
                            conn.close()
                            print('Close connection by client')
                            break
                    except socket.timeout:
                        print('Timeout error')
                        conn.close()
                    except socket.error:
                        conn.close()

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
    serv = Server(5)
    serv.running()
