from socket import *
from datetime import datetime, timedelta

def add_hours(number_of_hours):
    return datetime.now() + timedelta(hours=number_of_hours)

s = socket(AF_INET, SOCK_STREAM)
s.bind(("192.168.30.5", 33333))
s.listen(5)
print("Waiting connection")
conn, add = s.accept()
print("Connection from ",add)
conn.send("Welcome, How can I help you?".encode())
while True:
    data = conn.recv(1024)
    data = data.decode()
    print(data)
    if data.startswith("CO"):
        conn.send(str(add_hours(0)).encode())
    elif data == "DE":
        conn.send(str(add_hours(7)).encode())
    elif data == "UK":
        conn.send(str(add_hours(6)).encode())
    elif data == "QUIT":
        break
    #else:
        #reply=input("Reply> ")
        #conn.send(reply.encode())

s.close()