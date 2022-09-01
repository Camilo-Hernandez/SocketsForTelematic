from socket import *
from sys import argv, exit

def main():
    if len(argv) != 2:
        print("[!] Use: SocketClientUDP.py [Port]")
        exit(1)

    c = socket (AF_INET,SOCK_DGRAM)
    while True:
        entrada = input("Request> ")
        c.sendto(entrada.encode(),("localhost", int(argv[1])))
        if entrada.upper() == 'QUIT': break
        data,remote_host = c.recvfrom(1024)
        print(data.decode())
        if data.decode().upper() == 'QUIT': break

    c.close()
    exit()

if __name__ == '__main__':
    main()