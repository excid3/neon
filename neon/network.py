import threading
import SocketServer
import socket


# Keep a queue of network commands in a dictionary with keys as window names
queue = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class UDPHandler(SocketServer.BaseRequestHandler):
    """
    This class is for handling any incoming messages
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        #print threading.currentThread().getName()
        #print "%s wrote:" % self.client_address[0]
        #print repr(data)

        for item in data.split("\n"):
            window, command, args = item.split(":", 2)
            window, command, args = window.strip(), command.strip(), eval(args)

            # Package command and arguments
            data = (command,args)

            # Append it to the dictionary
            if window in queue: queue[window].append(data)
            else:               queue[window] = [data]

        #print queue
        socket.sendto("Okay", self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


def send_network_data(data, host):
    sock.sendto(data + "\n", host)
