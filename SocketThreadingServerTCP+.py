from ast import arg
from socketserver import ThreadingTCPServer, BaseRequestHandler
from sys import argv, exit

class myHandler(BaseRequestHandler):
    def handle(self):
        print ("Connection from ", str(self.client_address))
        while True:
            data = self.request.recv(1024).strip()
            if data.decode() == "bye\r\n": break
            self.request.send(data.upper())
        self.request.close()

def main():
    if len(argv) != 2:
        print("[!] Use: SocketThreadingServerTCP+.py [Port]")
        exit(1)
    myServer = ThreadingTCPServer(("127.0.0.1", int(argv[1])), myHandler)
    myServer.serve_forever()

if __name__ == '__main__':
    main()