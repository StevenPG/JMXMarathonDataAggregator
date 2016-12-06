FROM python:3
MAINTAINER Steven Gantz

#Download necessary files
RUN curl -o /jmxmarathondataaggregator.py https://gitlab.com/StevenPG/JMXMarathonDataAggregator/raw/master/jmxmarathondataaggregator.py
RUN curl -o /commandlineargumentshandler.py https://gitlab.com/StevenPG/JMXMarathonDataAggregator/raw/master/commandlineargumentshandler.py
RUN curl -o /marathonrestservice.py https://gitlab.com/StevenPG/JMXMarathonDataAggregator/raw/master/marathonrestservice.py
RUN curl -o /marathontcp.py https://gitlab.com/StevenPG/JMXMarathonDataAggregator/raw/master/marathontcp.py
RUN curl -o /serverhandler.py https://gitlab.com/StevenPG/JMXMarathonDataAggregator/raw/master/serverhandler.py
RUN curl -o /expose_metrics.py https://gitlab.com/StevenPG/JMXMarathonDataAggregator/raw/master/expose_metrics.py
RUN curl -o /metrics_obj.py https://gitlab.com/StevenPG/JMXMarathonDataAggregator/raw/master/metrics_obj.py

RUN chmod 777 *.py

ENV MARATHON_URL=default
ENV APP_ID=default
ENV MAX_SCALED_INSTANCES=default

CMD python jmxmarathondataaggregator.py ${MARATHON_URL} ${APP_ID} ${MAX_SCALED_INSTANCES}