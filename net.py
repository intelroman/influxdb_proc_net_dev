#!/usr/bin/python3
import os
import csv
import time
import multiprocessing
from pprint import pprint
from influxdb import InfluxDBClient

host = '127.0.0.1'
username = 'admin'
password = 'yourpassword'

client = InfluxDBClient(host=host, port=8086, username=username, password=password)
client.switch_database('stats')

##################################################
### Get the information from  /proc/net/dev
### Ouput example
###  face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
### vNic_8       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0

date = os.popen("date +%s").read().split('\n')
time = ((int(date[0])) * 1000000000 - 10000000000)
hn = os.popen("hostname").read().split('\n')
net = os.popen("cat /proc/net/dev | tail -n +3| sed -e \'s/[[:space:]]\+/,/g\'| sed -e \'s/^,//g\'| sed -e \'s/://g\'").readlines()
net = [i.rstrip('\n') for i in net]
pr={}
for row in csv.reader(net):
     pr['%s' % row[0]] = {'bytes_rx': row[1], 'pkt_rx': row[2], 'errs_rx': row[3], 'drop_rx': row[4], 'fifo_rx': row[5], 'frame_rx': row[6], 'compressed_rx': row[7], 'mulicats_rx': row[8], 'bytes_tx': row[9], 'pkt_tx': row[10], 'errs_tx': row[11], 'drop_tx': row[12], 'fifo_tx': row[13], 'colls_tx': row[14], 'carrier_tx': row[15], 'compressed': row[16]}

for p in pr.keys():
    for x,y in pr[p].items():
        pr[p][x] = int(y)

netdev = []
for i in pr.keys():
	netdev.append(i)
influx_data = []
for i in netdev:
	influx_data.append(
		{
			"measurement": "netdev",
			"tags": {
				"hostname" : hn[0],
				"dev" : i
			},
			"time": time,
			"fields": pr[i]
			}
			)
#pprint (influx_data)
client.write_points(influx_data)
