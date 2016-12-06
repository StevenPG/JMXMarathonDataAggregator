"""
metrics_obj.py
Author: Steven Gantz
Date: 12/6/2016

This class contains data related the application metrics. It is updated by individual
TCP Servers in their own threads. Each element in this object is unique per thread,
making the class threadsafe.
"""

import socket

class Metrics:
    """ Contains relevant data dynamically """

    def __init__(self):
        """ Initialize variables to contain data """
        self.server_list = []

    def add_server(self, data):
        """ Add a server to the active list to be presented"""
        self.server_list.append(data)

    def __str__(self):
        return socket.gethostname() + " reading: " + str(self.server_list)