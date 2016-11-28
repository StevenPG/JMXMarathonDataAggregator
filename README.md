# JMXMarathonDataExporter

This script was designed to be used with [Marathon](https://mesosphere.github.io/marathon/),
[Prometheus](https://prometheus.io/),
and the [JMXExporter](https://github.com/prometheus/jmx_exporter) project to 
allow Prometheus to retrieve data from multiple instances of a container 
created through Marathon.

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
