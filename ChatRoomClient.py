from threading import Thread
from urllib import response
from sys import argv, exit
from socket import *
import os
import telnetlib

if __name__ == '__main__':
    os.system('clear')
    if len(argv) != 3:
        print("[!] Use: SocketClientTCP.py [IP] [Port]")
        exit(1)
       
    class User:
        def __init__(self, server_ip: str, server_port: str) -> None:
            self.server_ip = server_ip
            self.server_port = int(server_port)
            self.userTCPsocket = socket(AF_INET, SOCK_STREAM)
            self.userTCPsocket.connect((self.server_ip, self.server_port))
            # 2 hilos paralelos: uno para enviar información constantemente, otro para recibir
            Thread(target=self.recv_from_TCPserver).start()
            Thread(target=self.send_to_TCPserver).start()

        def send_to_TCPserver(self):
            # Función de envío de datos activada en un hilo
            while True:
                request=input()
                if request.upper().startswith('CONN '):
                    try:
                        _, remote_ip = request.split(' ')
                        self.connect_to_udp_user(remote_ip=remote_ip)
                    except:
                        print("[!] CONN ERROR: Ingrese bien los datos.")
                        continue
                elif request.upper().strip() == 'WAIT':
                    self.wait_for_udp_user()
                self.userTCPsocket.send(request.encode())
                if request.upper().strip() == "BYE":
                    break
            self.userTCPsocket.close()

        def recv_from_TCPserver(self):
            # Función de recepción de datos activada en un hilo
            while True:
                response = self.userTCPsocket.recv(10000).decode().strip()
                if response.strip().startswith('BYE'): break
                print(response)
            self.userTCPsocket.close()
            exit(1)

        def connect_to_udp_user(self, remote_ip: str) -> None:
            self.remote_port = 7000
            self.userUDPsocket = socket(AF_INET, SOCK_DGRAM)
            print(f'Connecting with ({remote_ip},{self.remote_port})...')
            while True:
                msg = input("You > ")
                self.userUDPsocket.sendto(msg.encode(), (remote_ip, self.remote_port))
                if msg.lower() == 'bye': break
                data, remote_host = self.userUDPsocket.recvfrom(2048)
                data = data.decode().strip()
                print(f'{remote_host} > {data}')
                if data == 'bye': break
            print('Chat closed.')
            self.userUDPsocket.close()

        def wait_for_udp_user(self) -> None:
            self.my_udp_port = 7000
            self.my_ip = 'localhost' # gethostbyname(gethostname()) # 
            self.userUDPsocket = socket(AF_INET, SOCK_DGRAM)
            self.userUDPsocket.bind((self.my_ip, self.my_udp_port))
            print(f"Escuchando por el puerto {self.my_udp_port}...")
            while True:
                data, remote_host = self.userUDPsocket.recvfrom(2048)
                data = data.decode().strip()
                print(f'{remote_host} > {data}')
                if data == 'bye': break
                msg = input("You > ")
                self.userUDPsocket.sendto(msg.encode(), remote_host)
                if msg == 'bye': break
            print('Chat closed.')
            self.userUDPsocket.close()

            

    server_ip = str(argv[1])
    server_port = int(argv[2])
    user = User(server_ip, server_port)

    '''
    while True:
        with socket(AF_INET,SOCK_STREAM) as c:
            c.connect((str(argv[1]), int(argv[2])))
            # Recibo (baile)
            data = c.recv(10000)
            print (data.decode())
            # Envío (baile)
            request=input("Request> ")
            c.send(request.encode())
            if request.upper() == "BYE": break'''