#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import xml.etree.ElementTree as ET
import re
import datetime

global target, appID, apiKey
target = 'https://api.octranspo1.com/v1.2/GetNextTripsForStopAllRoutes'
appID = 'xxxxxxxx' #Replace with your app ID given by oc transpo
apiKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'   #Replace with apiKey from oc transpo
x = 0

def get_interest():
    stopNo =  raw_input("Enter Stop Number (or q to quit): ")
    if stopNo[:1] =='q' or stopNo[:1] =='Q':
        pass
    else:
        pull_times(stopNo)
        get_interest()


def pull_times(stopNo):
    global target, appID, apiKey
    print ""
    u = urllib2.urlopen(target, 'appID='+appID+'&apiKey='+apiKey+'&stopNo='+stopNo)
    doc = u.read()
    data = ET.fromstring(doc)

    for route in data.findall(".//{http://tempuri.org/}Route"):
        routeNo = route.find("{http://tempuri.org/}RouteNo").text
        routeHeading = route.find("{http://tempuri.org/}RouteHeading").text
        print 'Route: '+routeNo+" - "+routeHeading
        for trip in route.findall(".//{http://tempuri.org/}Trip"):
            adjust = trip.find("{http://tempuri.org/}AdjustedScheduleTime").text
            now = datetime.datetime.now() + datetime.timedelta(minutes=int(adjust))
            time = now.strftime("%H:%M")
            print time+', Arrives in: '+adjust+' minutes'
        print ""
    print ("\n")


if __name__ == '__main__':
        get_interest()