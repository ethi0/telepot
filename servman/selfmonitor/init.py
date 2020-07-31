import battery
import cpu
import disk
import csv

import os.path
from os import path


def Scan(bot, adminchatid, sysinfo_path):
    if path.exists(sysinfo_path) is False:
        battery_report = battery.Scan()
        cpu_report = cpu.Scan()
        with open(sysinfo_path, 'w', newline='') as csvfile:
            fieldnames = ['BATTERY', 'CPU']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'BATTERY': battery_report, 'CPU': cpu_report})
    else:
        print("Skipping scan...")
    
    