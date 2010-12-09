#!/usr/bin/env python

import sys

from OpenGL.GL import *
from OpenGL.GLUT import *

import threading
from socket import *


host = 'cluster-5.local'
port = 50000
buf = 1024

addr = (host, port)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(addr)
    

update = True


def main():
    
    # Initialize OpenGL
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    
    # Configure the display output
    glutGameModeString("2560x1024:24@60")
    glutEnterGameMode()
    
    # Setup callbacks
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    
    # Begin
    glutMainLoop()
    
    
def keyboard(key, x, y):
    if key == 'q':
        sock.send("quit\n")
        sys.exit(0)
        
        
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glBegin(GL_LINES)
    glVertex2f(-1.0, -1.0)
    glVertex2f(1.0, 1.0)
    
    glVertex2f(-1.0, 1.0)
    glVertex2f(1.0, -1.0)
    glEnd()
    
    glutSwapBuffers()
    
    
def process(sock):
    sock.send("render\n")
    
    print "Socket listening"
    
    while update:
        data = sock.recv(1024)

        if not data or data == "bye\n":
            break
            
        print data
            
    print "Socket closed"
    sock.close()
    

if __name__ == "__main__":    
    threading.Thread(target=process, args=(sock,)).start()
    main()
