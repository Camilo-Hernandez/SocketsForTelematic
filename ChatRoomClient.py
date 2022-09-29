from threading import Thread
from sys import argv, exit
from socket import *
import os

if __name__ == '__main__':
    os.system('clear')
    if len(argv) != 3:
        print("[!] Use: ChatRoomClient.py [Server IP] [Port]")
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
                request=input("\nRequest> ")
                if request.upper().startswith('CONN '):
                    try:
                        _, remote_ip = request.split(' ')
                        self.connect_to_udp_user(remote_ip=remote_ip)                    
                    except:
                        print("[!] CONN ERROR: Ingrese bien los datos.")
                        continue
                elif request.upper().strip().startswith('WAIT '):
                    try:
                        _, my_ip = request.split(' ')
                        self.wait_for_udp_user(my_ip)
                    except:
                        print("[!] CONN ERROR: Ingrese bien los datos.")
                        continue
                self.userTCPsocket.send(request.encode())
                if request.upper().strip() == "BYE":
                    print('Todo bien.')
                    break
                elif request.upper().strip() in ('LS','LSM') or request.upper().startswith('REG '): continue
                else: print('Lo que enviaste no hace nada.')
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
            print(f'Connected with ({remote_ip},{self.remote_port}). Start talking. Write "bye" to exit.')
            while True:
                # Encriptación del mensaje
                msg = input("You > ")
                self.encrypted_msg = ''
                for i in range(len(msg)):
                    self.encrypted_msg = self.encrypted_msg + chr(ord(msg[i])+3)
                else:
                    print(f'Encrypted: {self.encrypted_msg}')
                    self.userUDPsocket.sendto(self.encrypted_msg.encode(), (remote_ip,self.remote_port))
                if msg.lower() == 'bye': break

                # Desencriptación del mensaje
                data, remote_host = self.userUDPsocket.recvfrom(2048)
                data = data.decode().strip()
                self.decrypted_msg = ''
                for i in range(len(data)):
                    self.decrypted_msg = self.decrypted_msg + chr(ord(data[i])-3)
                else:
                    print(f'{remote_host} > {self.decrypted_msg}')
                    if self.decrypted_msg == 'bye': break
                    print()
            print('Chat closed.')
            self.userUDPsocket.close()

        def wait_for_udp_user(self, my_ip) -> None:
            self.my_udp_port = 7000
            self.my_ip = my_ip # gethostbyname(gethostname()) # 
            self.userUDPsocket = socket(AF_INET, SOCK_DGRAM)
            self.userUDPsocket.bind((self.my_ip, self.my_udp_port))
            print(f"Esperando en {self.my_ip}#{self.my_udp_port}...")
            while True:
                # Desencriptación del mensaje
                data, remote_host = self.userUDPsocket.recvfrom(2048)
                data = data.decode().strip()
                self.decrypted_msg = ''
                for i in range(len(data)):
                    self.decrypted_msg = self.decrypted_msg + chr(ord(data[i])-3)
                else:
                    print(f'{remote_host} > {self.decrypted_msg}')
                    if self.decrypted_msg == 'bye': break
                    print()
                if self.decrypted_msg == 'bye': break

                # Encriptación del mensaje
                msg = input("You > ")
                self.encrypted_msg = ''
                for i in range(len(msg)):
                    self.encrypted_msg = self.encrypted_msg + chr(ord(msg[i])+3)
                else:
                    print(f'Encryped: {self.encrypted_msg}')
                    self.userUDPsocket.sendto(self.encrypted_msg.encode(), remote_host)
                if msg == 'bye': break
            print('Chat closed.')
            self.userUDPsocket.close()

    server_ip = str(argv[1])
    server_port = int(argv[2])
    user = User(server_ip, server_port)