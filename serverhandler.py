"""
serverhandler.py
Author: Steven Gantz
Date: 11/22/2016

This script spins up individual socket servers on the local machine that
are listening on 0.0.0.0. Each socket server has an individual port which
maps directly to each scaled instance of an application inside Marathon.
"""

# Official Imports
from threading import Thread
import http.server

# Local Imports
from marathontcp import MarathonRedirectTCPServer
from marathontcp import MarathonRedirectTCPHandler

class ServerHandler:
    """ Handles spinning up multiple socker servers on httpserver to listen for requests """

    def __init__(self, inputArgs, marathon_service, metrics):
        """ Takes a CommandLineArguments object as input """
        self.inputArgs = inputArgs # Save CLA internally
        self.startingport = 4000 # Set default port
        self.metrics = metrics # Add metrics object
        self.marathon_service = marathon_service # get marathon data values
        self.__buildUsingValues()
        self.Handler = http.server.SimpleHTTPRequestHandler

    def __buildUsingValues(self):
        """ Build using individual values """
        startingPort = self.startingport
        endingPort = startingPort + int(self.inputArgs.totalports)

        self.threadList = []

        # Pass the URL into the TCP custom object
        index = 0
        for port in range(startingPort, endingPort):
            try:
                httpd = MarathonRedirectTCPServer(("0.0.0.0", port),
                                              MarathonRedirectTCPHandler, api_url=self.marathon_service.endpointList[index])

                # Add server to list of live endpoints
                self.metrics.add_server(self.marathon_service.endpointList[index])

                self.threadList.append(Thread(target=httpd.serve_forever))
                index = index + 1 # Iterate endpoint index
            except IndexError:
                print("Attempted to create thread with no live endpoint mapping.\n Thread " + str(index+1) + " creation denied.")
                index = index + 1

    def startSocketServers(self):
        """ Start and subsequently join the socket servers """
        # Start every thread on its own
        for thread in self.threadList:
            print("Starting " + str(thread))
            thread.start()

        # Join each thread
        for thread in self.threadList:
            thread.join()
            print(str(thread) + " joined")

