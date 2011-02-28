import threading
import SocketServer
import socket

queue = []
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class UDPHandler(SocketServer.BaseRequestHandler):
    """
    This class is for handling any incoming messages
    """
    
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        #print threading.currentThread().getName()
        #print "%s wrote:" % self.client_address[0]
        #print repr(data)
        
        for item in data.split("\n"):
            queue.append(item)
        
        #print queue
        socket.sendto("Okay", self.client_address)
        
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass
    

def send_network_data(data, host):
    #print host, data
    sock.sendto(data + "\n", host)
