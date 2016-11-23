"""
JMXMarathonDataAggregator.py
Author: Steven Gantz
Date: 11/22/2016

This script was designed to be used with Marathon, Prometheus,
and the JMXExporter project to allow Prometheus to retrieve data
from multiple instances of a java container created through Marathon.

Prometheus is unable to view each of these individual instances when
they are hidden behind a proxy and/or load balancer. The only data that
is passed depends on which container Prometheus hits when making a request.

This application can be run from any location, and is given a Marathon url.
The REST Api is then queried and the actual machinename:port is retrieved.
The app will then retrieve the data from every available machine:port/metrics
endpoint and port them to a preset list of ports.

Usage: python3 JMXMarathonDataAggregator.py <marathonurl> <appid> \
    <initialport> <totalports>
    OR
Usage: python3 JMXMarathonDataAggregator.py <marathonurl> \
    <appid> <list_of_ports>

marathonurl:   Full URL of marathon instance whose API will be queried
appid:         Full Appid to use within the REST Api calls
initialport:   Which port to start with (ex. 4010, 4011, 40<totalports>)
totalports:    Total number of ports to expose
# TODO - list_of_ports: comma seperated list with exact ports to expose
# TODO - figure out how to handle multiple ports inside each container - For now use first one in portlist
# TODO - Can also be read from a JMXAggregator.properties file.
# TODO - Crack into smaller individual modules
# TODO - Add refresh rate

The License for this application is located at the bottom of the file.
"""

import sys                        # Command line arguments
import requests                   # REST calls to Marathon
import json                       # Parse Marathon JSON Response
import http.server                # HTTP server to listen for requests
import socketserver               # Socket to handle incoming requests
from threading import Thread      # Individual threads for each http daemon

# EXISTS ONLY FOR TESTING PURPOSES #
sys.argv = ["http://wchvilsgrid03.qvcdev.qvc.net:8080/", "/apps/enableit/portal/enableportal-dev", 4010, 5]
#sys.argv = ["http://wchvilsgrid03.qvcdev.qvc.net:8080/", "/apps/enableit/portal/enableportal-dev", "[4010, 4011]"]
# END TESTING AREA #

def usageCheck():
    """ Run at the start of the application for verify structure """
    # Check python version 3 is being used
    if sys.version_info[0] < 3:
        print("You must use Python 3 to run this script.")
        sys.exit(1)

    # Verify command line arguments
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python3 JMXMarathonDataAggregator.py <marathonurl> " +
              "<appid> <initialport> <totalports>")
        print("OR: python3 JMXMarathonDataAggregator.py <marathonurl> " +
              "<appid> <list_of_ports>")
        exit(1);

class CommandLineArguments:
    """ Command line arguments object for easy reading """
    
    def __init__(self):
        """ Constructor builds the whole object """
        self.totalArgs = len(sys.argv)
        self.marathonURL = sys.argv[0]
        self.appid = sys.argv[1]
        if len(sys.argv) == 3: # If portlist was input
            self.portlist = sys.argv[2]
        elif len(sys.argv) == 4: # If starting and total ports was input
            self.startingport = sys.argv[2]
            self.totalports = sys.argv[3]

    def __str__(self):
        """ Python toString command for easy debugging """
        if len(sys.argv) == 3:
            return "CLA obj [" + self.marathonURL + ", " + \
                self.appid + ", " + self.portlist + "]"
        elif len(sys.argv) == 4:
            return "CLA obj [" + self.marathonURL + ", " + \
                self.appid + ", " + str(self.startingport) + ", " + \
                str(self.totalports) + "]"

class MarathonRestService:
    """ Contains reusable rest calls """
    
    def __init__(self, URL, ID):
        """ Save the marathon URL and appid internally """
        self.URL = URL
        self.ID = ID
        self.APISTR = "/v2/apps/"
        self.APP_REQ = (self.URL + self.APISTR + self.ID).replace("//", "/").replace("http:/", "http://")
        
        response = requests.get(self.APP_REQ)
        response_as_json = json.loads(response.text)
        self.totalScaledInstances = response_as_json['app']['instances']
        self.fullEndpointList = response_as_json['app']['tasks']
        
        # NOTE, CURRENTLY THE FIRST PORT IS CHOSEN AS THE JAVA EXPOSED PORT
        self.endpointList = []
        for endpoint in list(self.fullEndpointList):
            self.endpointList.append(endpoint['host'] + ":" + str(endpoint['ports'][0]))    

class MarathonRedirectTCPServer(socketserver.TCPServer):
    """ TCP Server that takes special extra arguments if needed """

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, api_url="Empty Request"):
        # As per http://stackoverflow.com/questions/15889241/send-a-variable-to-a-tcphandler-in-python
        self.api_url = api_url
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)    

class MarathonRedirectTCPHandler(socketserver.BaseRequestHandler):
    """ Makes a metrics request and forwards to preset ports through the application"""
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.request.sendall(str(self.server.api_url).encode())
        
class ServerHandler:
    """ Handles spinning up multiple socker servers on httpserver to listen for requests """

    def __init__(self, inputArgs, marathon_service):
        """ Takes a CommandLineArguments object as input """
        self.inputArgs = inputArgs # Save CLA internally
        self.marathon_service = marathon_service # get marathon data values
        if inputArgs.totalArgs == 3:
            self.__buildUsingPortlist()
        else: # 4 CLA means use starting and total ports
            self.__buildUsingValues()
        self.Handler = http.server.SimpleHTTPRequestHandler

    def __buildUsingPortlist(self):
        """ Build the servers using the portlist """
        pass

    def __buildUsingValues(self):
        """ Build using individual values """
        startingPort = self.inputArgs.startingport
        endingPort = startingPort + self.inputArgs.totalports

        self.threadList = []

        # Pass the URL into the TCP custom object
        index = 0
        for port in range(startingPort, endingPort):
            try:
                httpd = MarathonRedirectTCPServer(("localhost", port),
                                              MarathonRedirectTCPHandler, api_url=self.marathon_service.endpointList[index])
                self.threadList.append(Thread(target=httpd.serve_forever))
                index = index + 1 # Iterate endpoint index
            except IndexError:
                print("Attempted to create thread with no endpoint mapping.\n Creation Failed")

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

# ------------------ Actual execution below ------------------
usageCheck()                                                         # Verify correct inputs entered
inputArgs = CommandLineArguments()                                   # Retrieve command line arguments
client = MarathonRestService(inputArgs.marathonURL, inputArgs.appid) # build marathon service
server = ServerHandler(inputArgs, client)                            # build initial server handler
server.startSocketServers()                                          # Kick off socket servers

""" LICENSE BELOW

MIT License

Copyright (c) 2016 Steven Gantz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
