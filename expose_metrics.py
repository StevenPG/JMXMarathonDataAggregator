"""
expose_metrics.py
Author: Steven Gantz
Date: 12/6/2016

This class contains data and an http server that will
have data added to it when by the individual server threads,
and will present this data on a specific port, 
"""

# Official Imports
import socketserver
import urllib.request
from threading import Thread
import http.server

class MetricsTCPServer(socketserver.TCPServer):
    """ TCP Server that takes special extra arguments if needed """

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, msg_obj="EmptyRequest"):
        # As per http://stackoverflow.com/questions/15889241/send-a-variable-to-a-tcphandler-in-python
        self.msg_obj = msg_obj
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)    

class MetricsTCPHandler(socketserver.BaseRequestHandler):
    """ Makes a metrics request and forwards to preset ports through the application"""
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.request.sendall(str(self.server.msg_obj).encode())

class MetricsHandler:
    """ This class will contain data points and an up to date metrics endpoint """
    
    def __init__(self, msg_obj_in):
        """ Kick off http daemon exposing metrics endpoint """
        print("Building Metrics Daemon...")
        httpd = MetricsTCPServer(("0.0.0.0", 5000), MetricsTCPHandler, msg_obj=msg_obj_in)
        Thread(target=httpd.serve_forever).start()