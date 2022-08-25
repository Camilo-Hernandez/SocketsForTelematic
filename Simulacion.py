#from unicodedata import name
from MyNetwork import *

def main():

    h1 = Node('Host1', 0xC0A80001, 0xFFFFFF00)
    h2 = Node('Host2', 0xC0A80002, 0xFFFFFF00)
    print(h1.__str__())
    print(h2.__str__())
    # a. Enviando y recibiendo un mensaje
    h1.send(0xC0A80002,'Mensaje 1')
    Node.link.reset()
    h2.recv()
    Node.link.status = False

if __name__ == '__main__':
    main()