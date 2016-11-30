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

## Containerization

There's an image located in this project's docker registry. 

The application is designed to auto-expose on port 4000 -> n, where n is 4000 + totalScaledInstances.

The run command is as follows: 
    
    docker run -p 4000:4000 -p 4001:4001 -p 4002:4002 -p 4003:4003 -p 4004:4004 -i -d <image>:<tag> <marathonurl> <appid> <totalScaledInstances>
    
You'll need to open ports equal to the total number of scaled instances.

## TODO
- Hold old data in memory to avoid having to wait for retrieval
- Pretty print JSON so endpoints are readable