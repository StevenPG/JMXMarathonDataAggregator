"""
JMXMarathonDataAggregator.py
Author: Steven Gantz
Date: 11/22/2016

This script was designed to be used with Marathon, Prometheus,
and the JMXExporter project to allow Prometheus to retrieve data
from multiple instances of a container created through Marathon.

Prometheus is unable to view each of these individual instances when
they are hidden behind a proxy and/or load balancer.

This application can be run from any location, and is given a Marathon url.
The REST Api is then queried and the actual machinename:port is retrieved.
The app will then retrieve the data from every available machine:port/metrics
endpoint and port them to a preset list of ports.

Usage: python3 JMXMarathonDataAggregator.py <marathonurl> <appid> \
    <initialport> <totalports> <list_of_ports>

marathonurl:   Full URL of marathon instance whose API will be queried
appid:         Full Appid to use within the REST Api calls
initialport:   Which port to start with (ex. 4010, 4011, 40<totalports>)
totalports:    Total number of ports to expose
list_of_ports: Python list with exact ports to expose

Can also be read from a JMXAggregator.properties file.

The License for this application is located at the bottom of the file.
"""



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
