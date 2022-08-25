#!/usr/bin/python3

from socket import *
from sys import argv,exit
import os

if len(argv) != 4:
    print("[!] Use: scan.py [IP_Address] [TCP_Port_Init] [TCP_Port_Final]")
    exit(1)
ip = str(argv[1])
port_init = int(argv[2])
port_final = int(argv[3])

for port in range(port_init, port_final+1):
    scanner = socket(AF_INET, SOCK_STREAM)
    scanner.settimeout(0.6)
    try:
        scanner.connect((ip, port))
        print ("[*] %s:%s open" % (ip,port))
    except:
        print ("[*] %s:%s close" % (ip,port))
scanner.close()