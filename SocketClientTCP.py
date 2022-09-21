from socket import *
from sys import argv, exit

def main():
    if len(argv) != 3:
        print("[!] Use: SocketClientTCP.py [IP] [Port]")
        exit(1)

    while True:
        c = socket(AF_INET,SOCK_STREAM)
        c.connect((str(argv[1]), int(argv[2])))
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