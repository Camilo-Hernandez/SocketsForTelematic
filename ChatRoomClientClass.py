from socketserver import ThreadingUDPServer, DatagramRequestHandler
from socket import *

class myUDPHandler:
    # TODO: Definir después de establecer conexión con el servidor
    pass

class Usuario:
    def __init__(self, nombre: str, edad: int, sexo: str, ubicacion: str, server_ip: str, server_port: str) -> None:
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
        self.ubicacion = ubicacion
        self.server_ip = server_ip
        self.service_port = int(server_port)
        self.userTCPsocket = socket(AF_INET, SOCK_STREAM)
        self.userTCPsocket.connect((self.server_ip, self.service_port))
        self.myUDPServer = ThreadingUDPServer('localhost', 8000)
    
    def registrarUsuario(self):
        pass

    def pedirLista():
        pass

    def invitarUsuario():
        pass

    def esperarInvitacion():
        pass

    def salir():
        pass