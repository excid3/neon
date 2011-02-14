import threading
import SocketServer

queue = []

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
        
        socket.sendto("Okay", self.client_address)
        
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass
