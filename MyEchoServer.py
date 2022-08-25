#!/usr/bin/python3
from sys import argv,exit
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
    def start (self):
        self.server.bind((self.ip,self.port))
        if self.protocol_type.upper() == 'TCP':
            self.server.listen(5)    
        print ("Waiting connection")
    
    def handlerRequests(self):
        if self.protocol_type.upper() == 'TCP':
            while True:
                conn, add = self.server.accept()
                data = conn.recv(1024)
                if data == 'quit\r\n'.lower():
                    self.stop()
                print ("Connection from", add)
                conn.send(data.upper())
                conn.close()
        elif self.protocol_type.upper() == 'UDP':
            while True:
                data,remote_host = self.server.recvfrom(9999) # Pregunta G
                print(data.decode())
                print(remote_host)
                #('127.0.0.1',40082)
                self.server.sendto("Ok, I got it".encode(),remote_host) # Pasar a pantalla D
                self.server.close()

    def stop (self):
        self.server.close()
        print ("Server down")

def main():
    if len(argv) != 3:
        print("[!] Use: scan.py [IP_Address] [TCP_Port]")
        exit(1)

    s = MyEchoServer("127.0.0.1", 9999, 'UDP')
    s.start()
    s.handlerRequests()

if __name__ == '__main__':
    main()