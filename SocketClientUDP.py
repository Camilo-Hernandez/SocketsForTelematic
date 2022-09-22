from socket import *
from sys import argv 

def main():
    if len(argv) != 2:
        print("[!] Use: SocketClientUDP.py [Port]")
        exit(1)

    c = socket (AF_INET,SOCK_DGRAM)
    service_port = int(argv[1])
    server_ip = 'localhost'
    while True:
        entrada = input("Request> ")
        c.sendto(entrada.encode(),(server_ip, service_port))
        if entrada.upper() == 'QUIT': break
        data,remote_host = c.recvfrom(1024) # 1024 es el tamaño del buffer
        print(data.decode())
        if data.decode().upper() == 'QUIT': break

    c.close()
    exit()

if __name__ == '__main__':
    main()