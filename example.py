#!/usr/bin/env python

import sys

from OpenGL.GL import *
from OpenGL.GLUT import *


def main():

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(800, 600)
	glutCreateWindow("WUT")

	glutDisplayFunc(display)

	glutMainLoop()


def display():

	glClear(GL_COLOR_BUFFER_BIT)

	glBegin(GL_LINES)
	glVertex2f(1.0, 1.0)
	glVertex2f(0.0, 0.0)
	glEnd()

	glutSwapBuffers()

	return

if __name__ == "__main__":
	main()
