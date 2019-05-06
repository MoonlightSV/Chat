import socket
import threading
import sys
import time


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            try:
                data = c.recv(1024)

                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                print("[" + str(a[0]) + "]=[" + str(a[1]) + "]=[" + itsatime + "]/", end="")
                print(data.decode("utf-8"))

                for connection in self.connections:
                    if connection != c:
                        connection.send(data)
            except:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        print('[ Server Started ]')
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            # cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            # print(str(a[0]) + ':' + str(a[1]), "connected")


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    join = False
    shutdown = False
    alias = ''

    def sendMsg(self):
        while True:
            if not self.join:
                self.sock.send(("[" + self.alias + "] => join chat ").encode("utf-8"))
                self.join = True
            try:
                message = input()

                if message != "":
                    self.sock.send(("[" + self.alias + "] :: " + message).encode("utf-8"))

                time.sleep(0.2)
            except:
                self.sock.send(("[" + self.alias + "] <= left chat ").encode("utf-8"))
                # self.shutdown = True
            # raise

        # self.sock.send(("[" + self.alias + "] :: " + input("")).encode("utf-8"))

    def __init__(self, address, name=str(socket.gethostbyname(socket.gethostname()))):
        self.sock.connect((address, 10000))

        self.alias = name

        iThread = threading.Thread(target=self.sendMsg)
        # iThread.daemon = True
        iThread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))


if len(sys.argv) == 3:
    client = Client(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 2:
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()
