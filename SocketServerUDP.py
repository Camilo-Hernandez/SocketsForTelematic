from socket import *
from datetime import datetime, timedelta

def add_hours(number_of_hours):
    return datetime.now() + timedelta(hours=number_of_hours)

s = socket (AF_INET,SOCK_DGRAM)
s.bind(("localhost",4444)) # Pregunta K y pasar a pantalla D
print("Waiting connection")
while True:
    data,remote_host = s.recvfrom(1024) # Pregunta G
    # remote_host -> ('127.0.0.1',40082)
    data = data.decode()
    print(data)
    if data.startswith("CO"):
        s.sendto(str(add_hours(0)).encode(),remote_host)
    elif data == "DE":
        s.sendto(str(add_hours(7)).encode(),remote_host)
    elif data == "UK":
        s.sendto(str(add_hours(6)).encode(),remote_host)
    elif data.upper() == "QUIT":
        break
    else:
        reply=input("Reply> ")
        s.sendto(str(reply).encode(),remote_host)
        if reply.upper() == 'QUIT': break

s.close()