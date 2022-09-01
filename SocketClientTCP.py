from socket import *
from sys import argv, exit

def main():
    if len(argv) != 2:
        print("[!] Use: SocketClientTCP.py [Port]")
        exit(1)

    while True:
        c = socket(AF_INET,SOCK_STREAM)
        c.connect(("localhost", int(argv[1])))
        request=input("Request> ")
        c.send(request.encode())
        if request.upper() == "QUIT": break
        data = c.recv(9999)
        print (data.decode())
        if data.decode().upper() == 'QUIT': break
        c.close()
    exit()


if __name__ == '__main__':
    main()