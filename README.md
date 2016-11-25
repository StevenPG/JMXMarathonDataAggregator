# JMXMarathonDataExporter

This script was designed to be used with [Marathon](https://mesosphere.github.io/marathon/),
[Prometheus](https://prometheus.io/),
and the [JMXExporter](https://github.com/prometheus/jmx_exporter) project to 
allow Prometheus to retrieve data from multiple instances of a container 
created through Marathon.

Prometheus is unable to view each of these individual instances when
they are hidden behind a proxy and/or load balancer.

This application can be run from any location, and is given a Marathon url.
The REST Api is then queried and the actual machinename:port is retrieved.
The app will then retrieve the data from every available machine:port/metrics
endpoint and port them to a preset list of ports.

Usage: 

    python3 JMXMarathonDataAggregator.py <marathonurl> <appid> \
    <initialport> <totalScaledInstances>
    
    OR

    python3 JMXMarathonDataAggregator.py <marathonurl> \
    <appid> <list_of_ports>
    
- marathonurl:             Full URL of marathon instance whose API will be queried

- appid:                   Full Appid to use within the REST Api calls

- initialport:             Which port to start with (ex. 4010, 4011, 40<totalports>)

- totalScaledInstances:    Total number of ports to expose based on max number of scaled instances

[] TODO - list_of_ports: comma seperated list with exact ports to expose

[] TODO - figure out how to handle multiple ports inside each container - For now use first one in portlist

[] TODO - Can also be read from a JMXAggregator.properties file.

[] TODO - Crack into smaller individual modules

[] TODO - Add refresh rate
