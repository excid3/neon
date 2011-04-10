# This script will generate lines to be drawn on a network app called "Network"
# You can send any function across with named parameters to the receiving app

import random
import socket
import sys
import time

HOST, PORT = 'cluster-3.local', 9999
data = 'Network: draw_line: {"points":(%i,0, 0,%i), "color":(0,100,0,255)}'

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
    i = random.randint(0, 600)

    # Send the information to the network node where the app is running
    sock.sendto(data % (i, i) + "\n", (HOST, PORT))

    # Wait for a second
    time.sleep(0.001)

    # Here we can print the sent and received data for debugging if we want
    #received = sock.recv(1024)

    #print "sent: %s" % data
    #print "received: %s" % received
