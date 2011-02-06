import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
    sock.sendto(data + "\n", (HOST, PORT))
    received = sock.recv(1024)

    print "sent: %s" % data
    print "received: %s" % received
