from influxdb import InfluxDBClient
import sys
import redis
import json
from datetime import date
client = InfluxDBClient('localhost', 8086, '', '', 'metering')
client.create_database('metering')
r_cli = redis.Redis(host='172.27.100.42')
for key in r_cli.scan_iter("ubique:users:*"):
    user = key.decode().split(":")[2]
    stat_obj = json.loads(r_cli.get(key))
    try:
        for dc, stat in stat_obj['stats'].items():
            if "address" in stat:
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
                            "avg": float(stat['stats']['avr']),
                            "min": float(stat['stats']['min']),
                            "max": float(stat['stats']['max']),
                            "jitter": float(stat['stats']['jitter']),
                            }
                        }
                    ]
                print(stat)
                client.write_points(json_body)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass

