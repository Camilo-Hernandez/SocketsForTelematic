#!bin/python3
from socketserver import StreamRequestHandler, BaseRequestHandler
import string

class myTCPHandler(BaseRequestHandler):
    SOCKETS_LIST = [] # Lista de sockets en la red

    def handle(self):
        self.SOCKETS_LIST.append(self.request)
        # Mensaje únicamente al host que lo envió
        self.request.send(b"You're connected to the chatserver\r\n")
        host, port = self.client_address # Se obtiene la IP y puerto del cliente
        msg = f"Client joined {self.client_address}\r\n"
        print(msg)
        while True:
            data = self.request.recv(1024) # Se recibe el dato
            if data.decode() == "bye\r\n": # Abandono del servicio
                msg = f"Client left {self.client_address}\r\n"
                self.SOCKETS_LIST.remove(self.request)
                print(msg)
                #self.print_sockets_list()
                break
            else: # Mensaje a todos por broadcast
                msg = f"[{host}:{port}] {data.decode()}"
                print(msg)
                #self.print_sockets_list()
    
    def print_sockets_list(self):
        print(self.SOCKETS_LIST)


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