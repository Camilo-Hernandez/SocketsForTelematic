from socketserver import ThreadingTCPServer,BaseRequestHandler
import socket
from sys import argv, exit
import re
import functools as ft

class myHandler(BaseRequestHandler):
    SOCKETS_LIST = [] # Lista de sockets en la red

    def broadcast_string(self, b_msg, skip_socket):
        '''
        Envía el mensaje a todos los nodos de la red excepto al enviador
        '''
        for socket in self.SOCKETS_LIST:
            if socket != myServer and socket != skip_socket:
                socket.send(b_msg.encode())
        print (b_msg)

    def handle(self):
        self.SOCKETS_LIST.append(self.request)
        # Mensaje únicamente al host que lo envió
        self.request.send(b"You're connected to the chatserver\r\n")
        host, port = self.client_address # Se obtiene la IP y puerto del cliente
        msg = f"Client joined {self.client_address}\r\n"
        self.broadcast_string(msg,self.request) # Se envía el mensaje a todos
        while True:
            data = self.request.recv(1024) # Se recibe el dato
            if data.decode() == "bye\r\n": # Abandono del servicio
                msg = f"Client left {self.client_address}\r\n"
                self.SOCKETS_LIST.remove(self.request)
                self.broadcast_string(msg,self.request)
                #self.print_sockets_list()
                break
            elif data.decode().startswith('s=>'): # Mensaje único al servidor
                msg = f"[{host}:{port}] {data.decode()}"
                print(msg)
            elif re.search('\d+ \d+',data.decode()): # La entrada son dos números
                nums = re.split('\s', str(data.decode()[:-2]))
                suma=ft.reduce(lambda acc, num: acc + int(num), nums, 0)
                self.request.send(f'La suma es: sum{tuple(map(lambda num: int(num), nums))}={suma}\n'.encode())
            else: # Mensaje a todos por broadcast
                msg = f"[{host}:{port}] {data.decode()}"
                self.broadcast_string(msg, self.request)
                #self.print_sockets_list()
    
    def print_sockets_list(self):
        print(self.SOCKETS_LIST)

if __name__ == '__main__':
    if len(argv) != 2:
        print("[!] Use: MyChatRoom.py [Port]")
        exit(1)
    chat_service_port = int(argv[1])
    global myServer
    hostname = socket.gethostname()
    ip_server = socket.gethostbyname(hostname)
    print(f'Server\'s IP: {ip_server}')
    # Para conectar un cliente al servidor, es necesario conocer su ip, la cual es generada automaticamente por docker
    with ThreadingTCPServer(('0.0.0.0',chat_service_port),myHandler) as myServer:
        myHandler.SOCKETS_LIST.append(myServer)
        print (f"ChatServerTCP started on port {chat_service_port}")
        print ('Waiting for connections')
        myServer.serve_forever()
