#!/usr/bin/env python

"""Generates the graphics"""

import socket

HOST = 'cluster-1.local'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def send(node, message):
    s.send("%s:%s\n" % (node, message))
    return s.recv(1024)

try:
#    f = open("example.py", "rb")
#    for line in [f.strip() for f in f.readlines()]:
#        #print line
        send("cluster-5.local", "((1.0, 1.0), (0.0, 0.0))")
        send("cluster-5.local", "((-1.0, -1.0), (0.0, 0.0))")
        send("cluster-5.local", "((-1.0, 1.0), (0.0, 0.0))")
        send("cluster-5.local", "((0.0, 0.0), (1.0, -1.0))")
except:
    pass
    
s.send("stop\n")
s.close()
