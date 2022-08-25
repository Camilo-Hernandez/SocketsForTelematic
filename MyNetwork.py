#!/usr/bin/python3
class Packet:
    """ Basic packet """
    def __init__(self,src,dst,data):
        self.src = src
        self.dst = dst
        self.data = data
    def __str__(self):
        return f'{hex(self.src)} | {hex(self.dst)} | {self.data}'

class Link:
    """ A simple link """
    def __init__(self):
        self.node1 = ""
        self.node2 = ""
        self.medium = []
    def __str__(self):
        return f"{hex(self.node1)}<->{hex(self.node2)}:{self.medium}"

class SuperLink(Link):
    """ SuperLink, a class built from Link"""
    def __init__(self, status = True):
        Link.__init__(self) #Link builder
        self.status = status
    def reset(self):
        del self.medium[:]
        print('Packets deleted from medium.')

class Node:
    """ This is a host """
    link = SuperLink()
    def __init__(self,name,address, mask):
        "Constructor de la clase"
        self.name = name
        self.address = address
        self.mask = mask
        self.network = self.address & self.mask
        self.type = "PC"
        print ("Creating node", self.name)

    def __str__(self) -> str:
        "Retorna: nombre | IP"
        return f'{self.name} | {hex(self.address)}'

    def send(self,dst,msg):
        if not self.link.status:
            print('Link no disponible.')
        else:
            dst_network = dst & self.mask
            if dst_network != self.network:
                print('Dst Node not in the same network.')
            else:
                if dst == self.address:
                    print('Can\'t send packet to the source node.')
                else:
                    pkt = Packet(self.address, dst, msg)
                    self.link.node1 = self.address
                    self.link.node2 = dst
                    self.link.medium.append(pkt)
                    print ("Sending", pkt)

    def recv(self):
        if (len(self.link.medium)!=0):
            if self.address != self.link.node2:
                print('Can\'t extract a packet that is not for me.')
            else:               
                rpkt=self.link.medium.pop()
                print (f"Message from {hex(rpkt.src)} -> {rpkt.data}")
        else:
            print ("Can't extract. Link is empty.")