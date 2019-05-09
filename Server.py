import socket
import time
import threading


class Server:
    clients = []

    def __init__(self, prot):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 9090
        if prot == 'TCP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            self.runTCP()
        elif prot == 'UDP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.host, self.port))
            self.runUDP()

    def handler(self, c, a):
        while True:
            try:
                data = c.recv(1024)

                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                print("[" + str(a[0]) + "]=[" + str(a[1]) + "]=[" + itsatime + "]/", end="")
                print(data.decode("utf-8"))

                for client in self.clients:
                    if client != c:
                        client.send(data)
            except:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.clients.remove(c)
                c.close()
                break

    def runTCP(self):
        print('[ TCP Server Started ]')
        print('Hosted by address: ', self.host)
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.start()
            self.clients.append(c)

    def runUDP(self):
        quit = False
        print('[ UDP Server Started ]')
        print('Hosted by address: ', self.host)
        while not quit:
            try:
                d, a = self.sock.recvfrom(1024)
                if a not in self.clients:
                    self.clients.append(a)

                itsatime = time.strftime("%d.%m.%Y-%H:%M:%S", time.localtime())

                print("[" + str(a[0]) + ':' + str(a[1]) + "]/[" + itsatime + "]/", end="")
                print(d.decode("utf-8"))

                for c in self.clients:
                    if a != c:
                        self.sock.sendto(d, c)
            except:
                print('[ Server Stopped ]')
                quit = True
        self.sock.close()


if __name__ == '__main__':
    prot = input('Выберите протокол (TCP/UDP): ')
    Server(prot)
