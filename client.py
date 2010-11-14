import socket

HOST = 'cluster-3.local'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

try:
	while 1:
		s.send(raw_input())
  		data = s.recv(1024)
  		#s.close()
  		print 'Received' , repr(data)
except:
	s.send("stop")
	s.close()
