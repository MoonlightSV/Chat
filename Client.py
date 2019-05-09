import socket
import threading
import time


class Client:
    quit = False
    join = False

    def recvMsg(self):
        while not self.quit:
            try:
                data = self.sock.recv(1024)
                print(data.decode('utf-8'))

                time.sleep(0.2)
            except:
                pass

    def recvfromMsg(self):
        while not self.quit:
            try:
                while True:
                    data, addr = self.sock.recvfrom(1024)
                    print(data.decode('utf-8'))

                    time.sleep(0.2)
            except:
                pass

    def __init__(self, prot, address, name):
        self.host = address
        self.port = 9090
        self.server = (self.host, self.port)
        self.alias = name
        if prot == 'TCP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.runTCP()
        elif prot == 'UDP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.connect((self.host, self.port))
            self.runUDP()

    def runTCP(self):
        iThread = threading.Thread(target=self.recvMsg)
        iThread.start()

        while not self.quit:
            if not self.join:
                self.sock.send(("[" + self.alias + "] => join chat ").encode("utf-8"))
                self.join = True
            try:
                message = input()

                if message != "":
                    self.sock.send(("[" + self.alias + "] :: " + message).encode("utf-8"))

                time.sleep(0.2)
            except:
                self.sock.sendto(("[" + self.alias + "] <= left chat ").encode("utf-8"), self.server)
                self.quit = True
        self.sock.close()

    def runUDP(self):
        iThread = threading.Thread(target=self.recvfromMsg)
        iThread.daemon = True
        iThread.start()

        while not self.quit:
            if not self.join:
                self.sock.sendto(("[" + self.alias + "] => join chat ").encode("utf-8"), self.server)
                self.join = True
            else:
                try:
                    message = input()
                    if message != "":
                        self.sock.sendto(("[" + self.alias + "] :: " + message).encode("utf-8"), self.server)

                    time.sleep(0.2)
                except:
                    self.sock.sendto(("[" + self.alias + "] <= left chat ").encode("utf-8"), self.server)
                    self.quit = True
        self.sock.close()


if __name__ == '__main__':
    prot = input('Выберите протокол (TCP/UDP): ')
    address = input('Введите IP-адрес сервера: ')
    name = input('Введите ник: ')
    Client(prot, address, name)
