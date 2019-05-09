import socket
import time
import threading


class Server:
    clients = []
    shutdown = False
    count = 0

    def __init__(self, prot):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 9090
        if prot == 'TCP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(self.count)
            self.runTCP()
        elif prot == 'UDP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.host, self.port))
            self.runUDP()

    def handler(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024)

                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                print("[" + str(addr[0]) + "]=[" + str(addr[1]) + "]=[" + itsatime + "]/", end="")
                print(data.decode("utf-8"))

                for client in self.clients:
                    if client != conn:
                        client.send(data)
            except:
                self.clients.remove(conn)
                conn.close()
                self.count -= 1
                if self.count < 1:
                    print('[ Server Stopped ]')
                    self.shutdown = True
                    self.sock.close()
                break

    def runTCP(self):
        print('[ TCP Server Started ]')
        print('Hosted by address: ', self.host)
        while not self.shutdown:
            try:
                conn, addr = self.sock.accept()
                cThread = threading.Thread(target=self.handler, args=(conn, addr))
                cThread.start()
                self.clients.append(conn)
                self.count += 1
            except:
                pass

    def runUDP(self):
        print('[ UDP Server Started ]')
        print('Hosted by address: ', self.host)
        while not self.shutdown:
            try:
                data, addr = self.sock.recvfrom(1024)
                if addr not in self.clients:
                    self.clients.append(addr)

                itsatime = time.strftime("%d.%m.%Y-%H:%M:%S", time.localtime())

                print("[" + str(addr[0]) + ':' + str(addr[1]) + "]/[" + itsatime + "]/", end="")
                print(data.decode("utf-8"))

                for client in self.clients:
                    if addr != client:
                        self.sock.sendto(data, client)
            except:
                print('[ Server Stopped ]')
                self.shutdown = True
        self.sock.close()


if __name__ == '__main__':
    prot = input('Выберите протокол (TCP/UDP): ')
    Server(prot)
