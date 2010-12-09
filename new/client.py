#!/usr/bin/env python

from socket import *

if __name__ == "__main__":
    host = 'localhost'
    port = 50000
    buf = 1024
    
    addr = (host, port)
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(addr)
    
    while 1:
        data = raw_input(">> ")
        if not data:
            break
        else:
            sock.send(data)
            data = sock.recv(buf)
            if not data:
                break
            else:
                print data

    sock.close()
