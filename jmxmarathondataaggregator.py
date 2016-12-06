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

Usage: python3 jmxmarathondataaggregator.py <marathonurl> <appid> <totalScaledInstances>

marathonurl:             Full URL of marathon instance whose API will be queried
appid:                   Full Appid to use within the REST Api calls
totalScaledInstances:    Total number of ports to expose based on max number of scaled instances

The License for this application is located at the bottom of the file.
"""
# Official Imports
import sys                        # Command line arguments

# Local Imports
from commandlineargumentshandler import CommandLineArgumentsHandler
from marathonrestservice import MarathonRestService
from serverhandler import ServerHandler
from expose_metrics import MetricsHandler
from metrics_obj import Metrics

def usageCheck():
    """ Run at the start of the application for verify structure """
    # Check python version 3 is being used
    if sys.version_info[0] < 3:
        print("You must use Python 3 to run this script.")
        sys.exit(1)

    # Verify command line arguments
    if len(sys.argv) != 4:
        print("Usage: python3 jmxmarathondataaggregator.py <marathonurl> <appid> <totalScaledInstances>")
        exit(1);
    print("Arguments verified... Initializing...")

usageCheck()                                                         # Verify correct inputs entered
inputArgs = CommandLineArgumentsHandler(sys.argv)                    # Retrieve command line arguments
metrics = Metrics()
client = MarathonRestService(inputArgs.marathonURL, inputArgs.appid) # build marathon service
server = ServerHandler(inputArgs, client, metrics)                   # build initial server handler
handler = MetricsHandler(metrics)                                       # Start up metrics endpoint
server.startSocketServers()                                          # Kick off socket servers

"""

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
