#!/usr/bin/env python

import socket
import threading


HOST = ''
PORT = 50000
SIZE = 1024

threads = []


class NeonClient(threading.Thread):
	"""Each Neon client is connected to the launch node via a socket thread"""


	def __init__(self, client, address):
		threading.Thread.__init__(self)

		self.conn = client
		self.address = address
		self.on = True

	
	def run(self):
		"""Receive information on the socket"""

		while self.on:
			data = self.conn.recv(SIZE)

			if data == "stop":
				self.on = False
				self.conn.close()


def main(host, port):
	"""Launcher main loop"""

	nodes = []

	# Initialize server socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(6)

	print "Listening for nodes..."

	try:
		while 1:
			client, address = s.accept()
			
			print "%s:%s connected" % address
	
			client = NeonClient(client, address)
			client.start()
			
			nodes.append(client)
	except:
		print
		print "Shutting down neon..."


if __name__ == "__main__":
	main(HOST, PORT)
