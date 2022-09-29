from threading import Thread
from urllib import response
from sys import argv, exit
from socket import *
import os
import string

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
                # Encriptación del mensaje
                msg = input("You > ")
                self.encrypted_msg = ''
                for i in range(len(msg)):
                    self.encrypted_msg = self.encrypted_msg + chr(ord(msg[i])+3)
                else:
                    print(f'Encryped: {self.encrypted_msg}')
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

        def wait_for_udp_user(self) -> None:
            self.my_udp_port = 7000
            self.my_ip = 'localhost' # gethostbyname(gethostname()) # 
            self.userUDPsocket = socket(AF_INET, SOCK_DGRAM)
            self.userUDPsocket.bind((self.my_ip, self.my_udp_port))
            print(f"Escuchando por el puerto {self.my_udp_port}...")
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

        def shift_n_letters(text, n):
            """Emplea encriptación Cesar: Desplaza cada caracter de un texto, n cantidad de letras

            Args:
                text (str): texto a encriptar
                n (int): factor de desplazamiento

            Returns:
                str: texto encriptado
            """
            # alphabet "abcdefghijklmnopqrstuvwxyz"
            intab = string.ascii_lowercase
            # alphabet shifted by n positions
            outtab = intab[n % 26:] + intab[:n % 26]
            # translation made b/w patterns
            trantab = str.maketrans(intab, outtab)
            # text is shifted to right
            return text.translate(trantab)

            

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