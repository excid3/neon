#!/usr/bin/env python

import socket
import threading


HOST = ''
PORT = 50000
SIZE = 1024

nodes = {}

class NeonClient(threading.Thread):
	"""Each Neon client is connected to the launch node via a socket thread"""


	def __init__(self, client, address):
		threading.Thread.__init__(self)

		self.conn = client
		self.address = address
		self.on = True

	
	def run(self):
		"""Receive information on the socket"""

		try:
			while self.on:
				data = self.conn.recv(SIZE).split(":", 1)


				# Command for another machine				
				if len(data) == 2:
					self.send_to_node(*data)
					self.conn.send("ok")



				# Command for server
				else:
					self.conn.send(data[0])

					if data[0] == "stop":
						self.on = False
		except Exception, e:
			print e

		self.conn.close()
		print "%s:%s closed connection" % self.address


	def send_to_node(self, node, command):
		"""Send a command to another node

           node is the hostname of the other machine
		"""
		ip = socket.gethostbyname(node)

		if ip in nodes:
			print nodes[ip]
		else:
			print "ERROR: %s not connected" % node		


def main(host, port):
	"""Launcher main loop"""


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
			
			nodes[address[0]] = client
	except:
		s.close()
		print
		print "Shutting down Neon..."


if __name__ == "__main__":
	main(HOST, PORT)
