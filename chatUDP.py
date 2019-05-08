import socket
import threading
import sys
import time


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clients = []

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.sock.bind((self.host, 10000))

    def run(self):
        quit = False
        print('[ Server Started ]')
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


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    join = False
    shutdown = False

    def recvMsg(self):
        while not self.shutdown:
            try:
                while True:
                    data, addr = self.sock.recvfrom(1024)
                    print(data.decode("utf-8"))

                    time.sleep(0.2)
            except:
                pass

    def __init__(self, address, name=str(socket.gethostbyname(socket.gethostname()))):
        self.sock.connect((address, 10000))
        self.sock.setblocking(False)
        self.server = (address, 10000)
        self.alias = name

        iThread = threading.Thread(target=self.recvMsg)
        iThread.start()

        while not self.shutdown:
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
                    self.shutdown = True

        iThread.join()
        self.sock.close()


if len(sys.argv) == 3:
    client = Client(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 2:
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()
