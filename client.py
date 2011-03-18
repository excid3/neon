import random
import socket
import sys
import time

HOST, PORT = 'cluster-3.local', 9999
data = 'Network: draw_line: {"points":(%i,0, 0,%i), "color":(0,100,0,255)}'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
    i = random.randint(0, 600)
    sock.sendto(data % (i, i) + "\n", (HOST, PORT))
    time.sleep(0.001)
    #received = sock.recv(1024)

    #print "sent: %s" % data
    #print "received: %s" % received
