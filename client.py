import socket
import sys
import random

HOST, PORT = sys.argv[1], 9999
data = 'Window Title: draw_line: {"points":(%i,0, 0,%i), "color":(0,0,0,255)}'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
    i = random.randint(0, 600)
    sock.sendto(data % (i, i) + "\n", (HOST, PORT))
    #received = sock.recv(1024)

    #print "sent: %s" % data
    #print "received: %s" % received
