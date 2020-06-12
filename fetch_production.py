#!/usr/bin/env python3
from influxdb import InfluxDBClient
from dotenv import load_dotenv
import os
import re
import urllib.request

load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_series = os.getenv("INFLUX_SERIES")

widget_url = os.getenv("WIDGET_URL")

with urllib.request.urlopen(widget_url) as response:
    js = response.read().decode('utf-8')

matches = re.search(r'var current = parseFloat\(\\"([0-9.,]+)', js)
production = float(matches.group(1).replace('.', '').replace(',', '.'))

client = InfluxDBClient(host=db_host, port=db_port)
client.switch_database(db_name)

results = client.query("SELECT production, rate from {:s} ORDER BY time DESC LIMIT 1".format(db_series))
previousPoint = next(results.get_points())
rate = round(abs(production - previousPoint['production']), 5)
jerk = round(rate - previousPoint['rate'], 5)

isRealValue = jerk > 2

client.write_points([{'measurement': db_series, 'fields': {'production': production, 'rate': rate}, 'tags': {'isRealValue': isRealValue}}], 's')
