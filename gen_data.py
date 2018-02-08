from influxdb import InfluxDBClient
import sys
import json
from datetime import date
import uuid

import users

endpoints = ['endpoint1', 'endpoint2', 'endpoint3', 'endpoint4', 'endpoint5', 'endpoint6']

client = InfluxDBClient('localhost', 8086, '', '', 'metering')
client.create_database('metering')

from datetime import timedelta
from datetime import datetime

startTime = None
# startTime = datetime(2017, 9, 1)  #.strftime('%Y-%m-%dT%H:%M:%SZ')

if startTime == None:
    delay = 30
    every = 0
    startTime = datetime.now()
else:
    delay = 0
    every = 30

currentTime = startTime

import math
from random import gauss
import pylab
my_mean = 10
my_variance = 2000

random_numbers = [gauss(my_mean, math.sqrt(my_variance)) + 145 for i in range(5000)]

pylab.hist(random_numbers,20)
pylab.xlabel('Number range')
pylab.ylabel('Count')
pylab.savefig('realRandomVariates.pdf')
pylab.savefig('realRandomVariates.png')
pylab.show()

while true:
    for user in users:
        for endpoint in endpoints:
            try:
                json_body = [
                    {
                        "measurement": "user_latency",
                        "tags": {
                            "endpoint": endpoint,
                            "dc": endpoint + '_dc',
                            "region": "us-west",
                            "user": user,
                            "address": user
                        },
                        "time": currentTime.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "fields": {
                            "latency": float(stat['stats']['avr']),
                            }
                        }
                    ]
                client.write_points(json_body)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                pass

    time.sleep(delay)
    currentTime = currentTime + timedelta(seconds=every)





