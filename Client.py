import socket
import threading
import time


class Client:
    shutdown = False
    join = False

    def recvMsg(self):
        while not self.shutdown:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))

    def __init__(self, prot, address, name):
        self.host = address
        self.port = 9090
        self.alias = name
        if prot == 'TCP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif prot == 'UDP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.host, self.port))

        iThread = threading.Thread(target=self.recvMsg)
        iThread.start()

        while not self.shutdown:
            if not self.join:
                self.sock.send(("[" + self.alias + "] => join chat ").encode("utf-8"))
                self.join = True
            else:
                try:
                    message = input()
                    if message != "":
                        self.sock.send(("[" + self.alias + "] :: " + message).encode("utf-8"))

                    time.sleep(0.2)
                except:
                    self.sock.send(("[" + self.alias + "] <= left chat ").encode("utf-8"))
                    self.shutdown = True

        self.sock.close()


if __name__ == '__main__':
    prot = input('Выберите протокол (TCP/UDP): ')
    address = input('Введите IP-адрес сервера: ')
    name = input('Введите ник:')
    Client(prot, address, name)
