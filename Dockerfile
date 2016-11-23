FROM python:3
MAINTAINER Steven Gantz

RUN curl -o /JMXMarathonDataAggregator.py https://gitlab.com/StevenPG/JMXMarathonDataAggregator/raw/master/JMXMarathonDataAggregator.py

RUN ls -la /

EXPOSE 4010
EXPOSE 4011
EXPOSE 4012
EXPOSE 4013
EXPOSE 4014

CMD [ "python", "./JMXMarathonDataAggregator.py", "http://wchvilsgrid03.qvcdev.qvc.net:8080/", "/apps/enableit/portal/enableportal-dev", "4010", "5" ] ]