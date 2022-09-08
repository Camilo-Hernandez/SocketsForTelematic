from socketserver import ThreadingTCPServer,BaseRequestHandler
import socket
from sys import argv, exit

class myHandler(BaseRequestHandler):
    SOCKETS_LIST = []

    def broadcast_string(self, b_msg, skip_socket):
        for socket in self.SOCKETS_LIST:
            if socket != myServer and socket != skip_socket:
                socket.send(b_msg.encode())
        print (b_msg)

    def handle(self):
        self.SOCKETS_LIST.append(self.request)
        self.request.send(b"You're connected to the chatserver\r\n")
        host, port = self.client_address
        msg = "Client joined " + str(self.client_address) + "\r\n"
        self.broadcast_string(msg,self.request)
        while True:
            data = self.request.recv(1024)
            if data.decode() == "bye\r\n":
                msg = "Client left" + str(self.client_address) + "\r\n"
                self.SOCKETS_LIST.remove(self.request)
                self.broadcast_string(msg,self.request)
                #self.print_sockets_list()
                break
            elif data.decode().startswith('s=>'):
                msg = "[%s:%s] %s" % (host, port, data.decode())
                print(msg)
            else:
                msg = "[%s:%s] %s" % (host, port, data.decode())
                self.broadcast_string(msg, self.request)
                #self.print_sockets_list()
    
    def print_sockets_list(self):
        print(self.SOCKETS_LIST)

def main():
    '''if len(argv) != 2:
        print("[!] Use: MyChatRoom.py [Port]")
        exit(1)'''
    port = 9874 #int(argv[1])
    global myServer
    hostname = socket.gethostname()
    ip_server = socket.gethostbyname(hostname)
    print(f'Server\'s IP: {ip_server}')
    # Para conectar un cliente al servidor, es necesario conocer su ip, la cual es generada automaticamente por docker
    myServer = ThreadingTCPServer(('0.0.0.0',port),myHandler)
    myHandler.SOCKETS_LIST.append(myServer)
    print ("ChatServer started on port %s" % port)
    myServer.serve_forever()

if __name__ == '__main__':
    main()