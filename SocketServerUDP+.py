from socketserver import UDPServer, BaseRequestHandler

class myHandler(BaseRequestHandler):
    def handle(self):
        print ("Connection from ", str(self.client_address))
        data, conn = self.request
        conn.sendto(data.upper(),self.client_address)

myServer = UDPServer(("127.0.0.1", 3456), myHandler)
myServer.serve_forever()