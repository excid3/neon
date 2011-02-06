#!/usr/bin/env python

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
        print threading.currentThread().getName()
        print "%s wrote:" % self.client_address[0]
        print repr(data)
        
        queue.append(data)
        socket.sendto("Okay", self.client_address)
        
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass        
        
def start_server(function):
    HOST, PORT = "localhost", 9999
    server = ThreadedUDPServer((HOST, PORT), UDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    
    server_thread.setDaemon(True)
    server_thread.start()
    
    try:
        function()
    finally:
        print "\nShutting down"
        server.shutdown()
