from influxdb import InfluxDBClient
import sys
import json
from datetime import date
import uuid

import users
    
client = InfluxDBClient('localhost', 8086, '', '', 'metering')
client.create_database('metering')

for user in users:
    try:
        json_body = [
            {
                "measurement": "user_latency",
                "tags": {
                    "endpoint": stat['endpoints'][0],
                    "dc": dc,
                    "region": "us-west",
                    "user": user,
                    "address": stat['address']
                },
                "time": date.fromtimestamp(int(stat_obj['timestamp'])/1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    "latency": float(stat['stats']['avr']),
                    }
                }
            ]
        client.write_points(json_body)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass

