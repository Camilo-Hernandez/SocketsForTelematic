#!/usr/bin/python3

from socket import *
from sys import argv,exit
import os

if len(argv) != 3:
    print("[!] Use: scan.py [IP_Address] [TCP_Port]")
    exit(1)
ip = str(argv[1])
port = int(argv[2])
scanner = socket(AF_INET, SOCK_STREAM)
scanner.settimeout(0.6) #
try:
    scanner.connect((ip, port))
    print ("[*] %s:%s open" % (ip,port))
except:
    print ("[*] %s:%s close" % (ip,port))
scanner.close()