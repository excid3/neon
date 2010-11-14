#!/usr/bin/env python

"""Generates the graphics"""

import socket

HOST = 'cluster-1.local'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

try:
	while 1:
		s.send("cluster-5.local:gl something")
  		data = s.recv(1024)
  		print 'Received' , repr(data)
except:
	s.send("stop")

s.close()
