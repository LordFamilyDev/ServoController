
# Simple UDP Listener
# Binds to specified port and listens for UDP data
# incomming data is stuffed into queue
#  Referenced issue: https://stackoverflow.com/questions/25245223/python-queue-queue-wont-work-in-threaded-tcp-stream-handler
import queue
import threading
import socketserver

class UDPServerThread(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, queue=None):
        self.queue = queue
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

class UDPDataHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.queue = server.queue
        super().__init__( request, client_address, server)

    def handle(self):
        data = self.request[0].strip()
        self.queue.put(data)

# For Testing
if __name__ == "__main__":
    import sys
    import socket

    
    HOST = "127.0.0.1"
    PORT = 1111
    q = queue.Queue()
    server = UDPServerThread((HOST, PORT), UDPDataHandler, queue=q)
    server_thread = threading.Thread(target=server.serve_forever)
    ip, port = server.server_address
    server_thread.daemon = True
    server_thread.start()


    while True:
        try:
            item = q.get(block=False)
            if(item):
                print(item)
                q.task_done()
                #q.join()
        except KeyboardInterrupt:
            server.shutdown()
            sys.exit(0)
        except queue.Empty:
            pass