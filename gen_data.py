from influxdb import InfluxDBClient
import sys
import json
from datetime import date
import uuid
import os
import time
from users import users

endpoints = ['endpoint1', 'endpoint2', 'endpoint3', 'endpoint4', 'endpoint5', 'endpoint6']

badUsers = ['9f2315d6-a811-4ef7-b760-2af000e9cb39',
  '21a317fc-ccb8-44fc-9cbe-7fd012a4bb7e',
  '6b52d8b7-146a-4b29-bc0e-098d3b5f40b0',
  'a5d074a0-e254-4a8b-9f54-b3e9dc6c22e5',
  'afb531ae-c834-4044-802f-cb713a169547',
  '87b80723-9800-4d68-84a8-1063d9f59354',
  '37b1df42-945f-44c5-9d5e-85ff4d3fddca',
  '9dec56aa-d56c-4e40-ad79-52faf4fdf1d6',
  '083271d5-b2cc-4331-a55a-f34cb50d346a',
  '5bf6b179-4684-4c27-9039-ae416bc57f12']

from datetime import timedelta
from datetime import datetime

startTime = None
startTime = datetime(2017, 9, 1)  #.strftime('%Y-%m-%dT%H:%M:%SZ')

if startTime == None:
    delay = 300
    every = 0
    startTime = datetime.now()
else:
    delay = 0
    every = 300

currentTime = startTime

import math
import random
from random import gauss
import pylab
my_mean = 10
my_variance = 1000

# pylab.hist(random_numbers,20)
# pylab.xlabel('Number range')
# pylab.ylabel('Count')
# pylab.savefig('realRandomVariates.pdf')
# pylab.savefig('realRandomVariates.png')
# pylab.show()

os.environ['NO_PROXY'] = 'localhost'
import requests
url = "http://localhost:9200/metering_index/pingdata"
# client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'metering')
# try:
#     client.create_database('metering')
# except:
#     print("Unexpected error:", sys.exc_info()[0])
#     pass 

while True:
    random_numbers = [gauss(my_mean, math.sqrt(my_variance)) + 45 for i in range(5000)]
    for user in users:
        try:
            json_body = []
            for endpoint in endpoints:
                i = random.randint(0, 5000)
                json_body =  {
                        "measurement": "user_latency",
                        "endpoint": endpoint,
                        "dc": endpoint + '_dc',
                        "region": "us-west",
                        "user": user,
                        "address": user,
                        "time": (currentTime + timedelta(seconds= random.randint(0,300))).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "latency": abs(round(random_numbers[i] + random.uniform(500, 1000) if user in badUsers else random_numbers[i], 2))
                    }
                requests.post(url, json=json_body)
            # client.write_points(json_body)
                # print(user + ":" + endpoint + ":" + str(json_body[0]['fields']['latency']))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass

    time.sleep(delay)
    currentTime = currentTime + timedelta(seconds= every if every != 0 else delay)
