#!/usr/bin/env python

"""
This application generates the graphics for the other nodes to render
"""

from socket import *

host = 'cluster-5.local'
port = 50000
addr = (host, port)

s = socket(AF_INET, SOCK_STREAM)
s.connect(addr)


s.send("app\n")

s.send("WHAT THE FUCK\n")
s.send("WHAT THE FUCK\n")
s.send("WHAT THE FUCK\n")
s.send("WHAT THE FUCK\n")


s.send("quit\n")
print s.recv(1024)
s.close()
