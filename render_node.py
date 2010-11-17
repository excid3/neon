import socket
import threading

HOST = 'cluster-1.local'
PORT = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

updates = True

lines = []


def get_updates():
    while updates:
        data = sock.recv(1024).strip()
        print 'Received', repr(eval(data))
        lines.append(eval(data))

    
    sock.send("stop\n")
    sock.close()
    
def idle():
    # check if we have new lines
    glutPostRedisplay()
    
from OpenGL.GL import *
from OpenGL.GLUT import *

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINES)
    for start, end in lines:
        glVertex2f(*start)
        glVertex2f(*end)
    glEnd()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow("WUT")
glutDisplayFunc(display)

# Use timer instead
glutIdleFunc(idle)

threading.Thread(target=get_updates).start()

glutMainLoop()

updates = False
