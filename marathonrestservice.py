"""
marathonrestservice.py
Author: Steven Gantz
Date: 11/22/2016

This class contains only a constructor that makes a service call to the input
marathon URL's REST API, resulting in class attributes that are easily
retrievable by other elements of the application.
"""

# Required official imports
import urllib.request
import json

class MarathonRestService:
    """ Contains reusable rest calls """
    
    def __init__(self, URL, ID):
        """ Save the marathon URL and appid internally """
        self.URL = URL
        self.ID = ID
        self.APISTR = "/v2/apps/"
        self.APP_REQ = (self.URL + self.APISTR + self.ID).replace("//", "/").replace("http:/", "http://")
        
        response = urllib.request.urlopen(self.APP_REQ)
        response_as_json = json.loads(response.read().decode('utf-8'))
        self.totalScaledInstances = response_as_json['app']['instances']
        self.fullEndpointList = response_as_json['app']['tasks']
        
        # NOTE, CURRENTLY THE SECOND PORT IS CHOSEN AS THE JMX EXPOSED PORT
        self.endpointList = []
        for endpoint in list(self.fullEndpointList):
            self.endpointList.append(endpoint['host'] + ":" + str(endpoint['ports'][1]))    

