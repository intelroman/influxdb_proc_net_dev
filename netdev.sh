#!/bin/bash 

influx_ip="123.123.123.123"
influx_user="user"
influx_pass="pass"
influx_db="stats"

data=`cat /proc/net/dev | tail -n +3| sed -e 's/[[:space:]]\+/ /g'| sed -e 's/^ //g'| sed -e 's/://g'`
host=`hostname`
t=($(date +%s%N))
feed="mem_info,host=$host $data $t"
echo "$data" | while read a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 a12 a13 a14 a15 a16 a17
do 
	z="RCVbytes=$a2,RCVpackets=$a3,RCVerrs=$a4,RCVdrop=$a5,RCVfifo=$a6,RCVframe=$a7,RCVcompressed=$a8,RCVmulticast=$a9,\
SNDbytes=$a10,SNDpackets=$a11,SNDerrs=$a12,SNDdrop=$a13,SNDfifo=$a14,SNDcolls=$a15,SNDcarrier=$a16,SNDcompressed=$a9" 
	feed="net_dev,host=$host,interface=$a1 $z $t"
	eval curl -u $influx_user:$influx_pass -i -XPOST 'http://$influx_ip:8086/write?db=$influx_db' --data-binary \' $feed \'
done

