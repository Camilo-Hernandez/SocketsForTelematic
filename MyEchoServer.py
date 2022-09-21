#!/usr/bin/python3
from sys import argv, exit
from socket import *

class MyEchoServer:
    def __init__(self,ip,port, protocol_type = 'TCP'):
        self.ip = ip
        self.port = port
        self.protocol_type = protocol_type
        if self.protocol_type.upper() == 'TCP':
            self.server = socket(AF_INET,SOCK_STREAM)
        elif self.protocol_type.upper() == 'UDP':
            self.server = socket(AF_INET,SOCK_DGRAM)
        else:
            print('Protocol not permitted.')
    
    def start (self):
        self.server.bind((self.ip, self.port))
        if self.protocol_type.upper() == 'TCP':
            self.server.listen(5)
        print ("Waiting connection")
    
    def handlerRequests(self):
        if self.protocol_type.upper() == 'TCP':
            while True:
                conn, remote_host = self.server.accept()
                print ("Connection from", remote_host)
                data = conn.recv(1024)
                conn.send(data.upper())
                if data.decode().lower() in ('quit\r\n', 'quit', 'quit\n'):
                    self.stop()
                    break
                conn.close()

        elif self.protocol_type.upper() == 'UDP':
            while True:
                data, remote_host = self.server.recvfrom(9999)
                # remote_host -> ('127.0.0.1',40082)
                print ("Connection from", remote_host)
                #print(data)
                self.server.sendto(data.upper(), remote_host)
                if data.decode().lower() in ('quit\r\n', 'quit', 'quit\n'):
                    self.stop()
                    break

    def stop (self):
        self.server.close()
        print ("Server down")

def main():
    if len(argv) != 4:
        print("[!] Use: MyEchoServer.py [Protocol_Type] [IP_Address] [Port]")
        exit(1)
    
    s = MyEchoServer(str(argv[2]), int(argv[3]), str(argv[1]))
    s.start()
    s.handlerRequests()

if __name__ == '__main__':
    main()