from socket import *
c = socket (AF_INET,SOCK_DGRAM)
entrada = input("Request> ")
c.sendto(entrada.encode(),("192.168.30.72",4444))
data,remote_host = c.recvfrom(1024)
print(data.decode())
c.close()
exit()