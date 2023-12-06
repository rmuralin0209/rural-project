import os
import psutil
import json
import subprocess
import time

def net_usage(inf, filename):   #change the inf variable according to the interface
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_1 = net_stat.bytes_recv
    net_out_1 = net_stat.bytes_sent
    time.sleep(1)
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_2 = net_stat.bytes_recv
    net_out_2 = net_stat.bytes_sent

    net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
    net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)

    if(net_in != 0 or net_out != 0):
        print(f"{inf} Current net-usage:\nIN: {net_in} MB/s, OUT: {net_out} MB/s")
        f.write(f"{inf} Current net-usage:\nIN: {net_in} MB/s, OUT: {net_out} MB/s \n")

with open("bandwidth.txt", "w") as f:
    for i in range(5):
        for elem in psutil.net_io_counters(pernic=True, nowrap=True):
            net_usage(elem, f)