"""
marathontcp.py
Author: Steven Gantz
Date: 11/22/2016

These two classes are used as custom TCP Servers and its accompanying
handler that defines each request. These class are what forward the data
from the preset /metrics endpoints in the scaled marathon instances directly
to the TCP servers running from this application.
"""

# Official Imports
import socketserver

class MarathonRedirectTCPServer(socketserver.TCPServer):
    """ TCP Server that takes special extra arguments if needed """

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, api_url="Empty Request"):
        # As per http://stackoverflow.com/questions/15889241/send-a-variable-to-a-tcphandler-in-python
        self.api_url = api_url
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)    

class MarathonRedirectTCPHandler(socketserver.BaseRequestHandler):
    """ Makes a metrics request and forwards to preset ports through the application"""
    
    def handle(self):
        # Make a request to the api_url metrics and fwd to page
        encoded_response = urllib.request.urlopen("http://" + self.server.api_url + "/metrics")
        
        # self.request is the TCP socket connected to the client
        self.request.sendall(encoded_response.read())
        
