from socketserver import ThreadingTCPServer, BaseRequestHandler, StreamRequestHandler
import socket
from sys import argv, exit
import re
import functools as ft
import pandas as pd
import hashlib


class myHandler(StreamRequestHandler):
    SOCKETS_LIST = []  # Lista de sockets en la red
    FEATURES = ('Name', 'Age', 'Sex', 'Location', 'Host', 'Port')
    REGISTER = pd.DataFrame(columns=FEATURES)

    def append_row(self, df, row):
        return pd.concat([
                    df,
                    pd.DataFrame([row], columns=row.index)]
            ).reset_index(drop=True)

    def broadcast_string(self, b_msg, skip_socket):
        '''
        Envía el mensaje a todos los nodos de la red excepto al enviador
        '''
        for socket in self.SOCKETS_LIST:
            if socket != myServer and socket != skip_socket:
                socket.send(b_msg.encode())
        print(b_msg)

    def handle(self):
        self.SOCKETS_LIST.append(self.request)
        # Mensaje únicamente al host que lo envió
        # Se obtiene la IP y puerto del cliente
        host, port = self.client_address
        host=str(host)
        port=str(port)
        # Informar nuevo usuario en la sala a todo el mundo
        self.notifyNewUser()
        # Enviar menú
        menu = '''
        Bienvenido a ChatRoom.
        Está conectado al servidor.
        Lista de comandos:
        REG <nombre> <edad> <sexo: M/F/NB> <ubicacion: MED, ENV, SAB, EST, BEL, ITA>
        CONN <hash-5 primeros dígitos>
        LS
        BYE
        '''
        self.request.send(menu.encode())
        while True:
            # Estar a la espera de conexión
            prompt = '\nRequest> '
            self.request.send(prompt.encode())

            data = self.request.recv(1024)
            command = data.decode()
            if command.upper() == "BYE\r\n":  # Abandono del servicio
                msg = f"Client left {self.client_address}\r\n"
                self.SOCKETS_LIST.remove(self.request)
                self.broadcast_string(msg, self.request)
                # self.print_sockets_list()
                break
            elif command.upper().startswith('REG '):  # Registro de usuario
                if not self.registerUser(command, host, port):
                    continue
            elif command.upper().startswith('CONN '):
                pass
            elif command.upper() == 'LS\r\n':
                self.sendList(host, port)
            else:  # Mensaje a todos por broadcast
                msg = f"[{host}:{port}] {command}"
                self.broadcast_string(msg, self.request)
                # self.print_sockets_list()

    def registerUser(self, command, host, port):
        _, name, age, sex, location = command.split(" ")
        location = location.strip()

        # Validación de edad
        if int(age) not in range(19, 100):
            msg = f'Estás demasiado joven para tomar, ubícate güevón.'
            self.wfile.write(msg.encode())
            return False

        # Validación de sexo
        if sex.upper() not in ('M', 'F', 'NB'):
            msg = f'Meta bien el sexo. Sólo se admiten humanos.'
            self.wfile.write(msg.encode())
            return False

        # Validación de ubicación
        if location.upper() not in ('MED', 'ENV', 'SAB', 'EST', 'BEL', 'ITA'):
            msg = f'Sólo personas en MED, ENV, SAB, EST, BEL, ITA'
            self.wfile.write(msg.encode())
            return False

        # Registro del usuario
        temp_code = command+host+port # para el hash
        id = hashlib.sha256(temp_code.encode('utf-8')).hexdigest()[:5] # hash id
        self.REGISTER.loc[id] = {f:r for f,r in zip(self.FEATURES, (name, age, sex, location, str(host), str(port) ))} # anexo al registro
        # Envío de los datos del usuario al propio usuario
        msg = map(lambda f,r: f'{f}: {r}\n'.encode(), self.FEATURES, self.REGISTER.loc[id])  # creación del iterador del mensaje
        list(map(self.wfile.write, msg)) # enviar mensaje
        # impresión del proceso
        log = f'Usuario {id} registrado'
        print(log)
        msg = f'{self.REGISTER.loc[id]}'
        print(msg)
        
    def sendList(self, host, port):
        log = f'Listando usuarios'
        print(log)
        for i in range(len(self.REGISTER)):
            # TODO: excluir el solicitante de la lista
            msg = map(lambda f,r: f'{f}: {r}\n'.encode(), self.FEATURES, self.REGISTER.iloc[i])
            list(map(self.wfile.write, msg))
            self.wfile.write(b'\n')

    def notifyNewUser(self):
        msg = f"\nUsuario conectado: {self.client_address}\r\n"
        self.broadcast_string(msg,self.request) # Se envía el mensaje a todos
        msg = "\nRequest> "
        self.broadcast_string(msg,self.SOCKETS_LIST[0]) # Se envía el mensaje a todos excepto al propio servidor

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
