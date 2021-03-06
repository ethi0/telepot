import battery
import cpu
import disk
import fans
import csv
import operator
import psutil
import os
from datetime import datetime
import os.path
from os import path



def eventReporter(bot, adminchatid, sysinfo_path):
    with open(sysinfo_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['BATTERY'] == '1':
                print("Battery exists, continue...")
                battery_report = battery.Monitor()
            elif row['BATTERY'] == '0':
                print("Battery doesn't exist, skipping.")
                battery_report = ""
    with open(sysinfo_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['TEMPERATURES'] == '1':
                print("Temperature sensor exists, continue...")
                cpu_heat_report = cpu.heatMonitor()
            elif row['TEMPERATURES'] == '0':
                print("Temperature sensor doesn't exist, skipping.")
                cpu_heat_report = ""

    cpu_load_report = cpu.loadMonitor()
    disk_report = disk.Monitor()
    report_list = [battery_report, cpu_load_report,
                   cpu_heat_report, disk_report]
    allow_report = 0
    for report in report_list:
        if report != "" and allow_report == 0:
            print("Report is preparing: " + report)
            allow_report = 1
    if allow_report == 1:
        for adminid in adminchatid:
            bot.sendMessage(adminid, battery_report + "\n" +
                            cpu_load_report + "\n" +
                            cpu_heat_report + "\n" +
                            disk_report)
    else:
        print("No changes.")


def statsReporter(bot, chat_id, sysinfo_path):
    items_list = []
    i = 0

    battenergy = ""
    battcharge = ""
    batttime = ""
    fanspeed = ""
    cputemp = ""
    with open(sysinfo_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            items_list.append(row)
        while i <= len(items_list):
            if items_list[1][i] == '1':
                print(items_list[0][i] + " exists, continue check...")
                if items_list[0][i] == 'BATTERY':
                    battery = psutil.sensors_battery()
                    battenergy = "Battery energy: %.2f percents" % battery.percent
                    battcharge = "Battery charging: " + str(battery.power_plugged)
                    batttime = "Battery time left: %.2f minutes" % (battery.secsleft / 60)
                elif items_list[0][i] == 'FANS':
                    fans = psutil.sensors_fans()
                    fanspeed = "FAN: %.0f RPM" % list(fans.values())[0][0][1]
                elif items_list[0][i] == 'TEMPERATURES':
                    cputemp = "CPU Temperature " + str(list(temperature.values())[0][0][1])    
            elif items_list[1][i] == '0':
                print(items_list[0][i] + " doesn't exist, skipping.")
            elif items_list[1][i] != '1' and items_list[1][i] != '0':
                print(str(items_list[0][i]) + " is not being checked for existence: " + str(items_list[1][i]))
            i += 1

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    cpufreq = psutil.cpu_freq()
    cpuperc = psutil.cpu_percent()
    temperature = psutil.sensors_temperatures()
    swap = psutil.swap_memory()
    loadavg = os.getloadavg()
    boottime = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    timedif = "Online for: %.2f Hours" % (
        ((now - boottime).total_seconds()) / 3600)
    memtotal = "Total memory: %.3f GB " % (memory.total / 1000000000)
    memavail = "Available memory: %.3f GB" % (
        memory.available / 1000000000)
    memuseperc = "Used memory: " + str(memory.percent) + " %"
    diskused = "Disk used: " + str(disk.percent) + " %"
    cpuperccurr = "CPU Load " + str(cpuperc.conjugate()) + " %"
    cpurfreqcurr = "CPU frequency: %.2f MHz" % cpufreq.current
   #cputemp = "CPU Temperature " + str(list(temperature.values())[0][0][1])
    swapused = "SWAP used " + str(swap.used / 1024 / 1024) + " MB"
    loadavgcurr = "Load AVG " + str(loadavg)
    pids = psutil.pids()
    pidsreply = ''
    procs = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            pmem = p.memory_percent()
            if pmem > 0.5:
                if p.name() in procs:
                    procs[p.name()] += pmem
                else:
                    procs[p.name()] = pmem
        except:
            print("Hm")
    sortedprocs = sorted(
    procs.items(), key=operator.itemgetter(1), reverse=True)
    for proc in sortedprocs:
        pidsreply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"
        reply = timedif + "\n" + \
            memtotal + "\n" + \
            memavail + "\n" + \
            memuseperc + "\n" + \
            diskused + "\n" + \
            loadavgcurr + "\n" + \
            cpuperccurr + "\n" + \
            cpurfreqcurr + "\n" + \
            cputemp + "\n" + \
            fanspeed + "\n" + \
            swapused + "\n" + \
            battenergy + "\n" + \
            battcharge + "\n" + \
            batttime + "\n\n" + \
            pidsreply
    bot.sendMessage(chat_id, reply, disable_web_page_preview=True)



def Scan(sysinfo_path):
    if path.exists(sysinfo_path) is False:
        battery_report = battery.Scan()
        cpu_report = cpu.ScanCpuCount()
        fans_report = fans.Scan()
        temp_report = cpu.ScanTempSensors()
        with open(sysinfo_path, 'w', newline='') as csvfile:
            fieldnames = ['BATTERY', 'CPU', 'FANS', 'TEMPERATURES']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'BATTERY': battery_report, 'CPU': cpu_report, 'FANS': fans_report, 'TEMPERATURES': temp_report})
    else:
        print("Skipping scan...")
