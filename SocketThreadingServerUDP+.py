from ast import arg
from socketserver import ThreadingUDPServer, BaseRequestHandler
from sys import argv, exit
import socket

class myHandler(BaseRequestHandler):
    def handle(self):
        print ("\n---> New Connection from ", str(self.client_address))
        while True:
            data, client_socket  = self.request[0], self.request[1]
            if data.decode() == "bye\r\n": break
            client_socket.sendto(data.upper(), self.client_address)
        self.request.close()

def main():
    if len(argv) != 2:
        print("[!] Use: SocketThreadingServerTCP+.py [Port]")
        exit(1)
    chat_service_port = int(argv[1])
    hostname = socket.gethostname()
    ip_server = socket.gethostbyname(hostname)
    print(f'Server\'s IP: {ip_server}')
    myServer = ThreadingUDPServer(("0.0.0.0", int(argv[1])), myHandler)
    print (f"UPPER ECHO UDP server started on port {chat_service_port}")
    myServer.serve_forever()

if __name__ == '__main__':
    main()