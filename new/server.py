#!/usr/bin/env python

import threading
from socket import *


render_nodes = {}


class NeonClient(threading.Thread):
    def __init__(self, client, addr):
        threading.Thread.__init__(self)
        self.conn = client
        self.addr = addr
        
    def run(self):
        while 1:
        
            # Wait until the client sends us something
            data = self.conn.recv(1024)

            if not data:
                break
            
            commands = data.split("\n")
            for cmd in [c.strip() for c in commands if c]:
                print repr(cmd)
                if cmd == "quit":
                    #TODO: use self.running?
                    print "%s:%d disconnected" % self.addr
                    self.conn.send("bye\n")
                    break

        
        self.conn.close()


if __name__ == "__main__":
    host = ''
    port = 50000
    buf = 1024
    
    addr = (host, port)
    
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(addr)
    server.listen(5)
    
    while 1:
        print "Server is listening for connections"
        
        sock, addr = server.accept()
        print "Accepted connection from: %s:%d" % addr
        
        
        node_type = sock.recv(buf).split("\n")[0]

        if node_type in ["render", "app"]:        
            print "Set %s:%d as %s node" % (addr[0], addr[1], node_type)
            
            client = NeonClient(sock, addr)
            client.start()

            if node_type == "render":
                render_nodes[addr] = client
            
            elif node_type == "app":
                pass
            
        else:        
            print "Invalid node type '%s' for %s:%d" % (node_type, addr[0], addr[1])
            
        
    server.close()
            
