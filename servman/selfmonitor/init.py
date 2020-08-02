import battery
import cpu
import disk
import fans
import csv

import os.path
from os import path


def Scan(bot, adminchatid, sysinfo_path):
    if path.exists(sysinfo_path) is False:
        battery_report = battery.Scan()
        cpu_report = cpu.Scan()
        fans_report = fans.Scan()
        with open(sysinfo_path, 'w', newline='') as csvfile:
            fieldnames = ['BATTERY', 'CPU', 'FANS']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'BATTERY': battery_report, 'CPU': cpu_report, 'FANS': fans_report})
    else:
        print("Skipping scan...")
    
    