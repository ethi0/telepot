import battery
import cpu
import disk
import csv


def Reporter(bot, adminchatid, sysinfo_path):
    with open(sysinfo_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['BATTERY'] == '1':
                print("Battery exists, continue...")
                battery_report = battery.Monitor()
            elif row['BATTERY'] == '0':
                print("Battery doesn't exist, skipping.")
                battery_report = ""

    cpu_load_report = cpu.loadMonitor()
    cpu_heat_report = cpu.heatMonitor()
    disk_report = disk.Monitor()
    report_list = [battery_report, cpu_load_report, cpu_heat_report, disk_report]
    allow_report = 0
    for report in report_list:
        print(report + str(allow_report))
        if report != "" and allow_report == 0:
            print("Report is preparing: " + report)
            allow_report = 1
        
    print("AllowReport is " + str(allow_report))
    if allow_report == 1:
        for adminid in adminchatid:
            bot.sendMessage(adminid, battery_report + "\n" + \
                cpu_load_report + "\n" + \
                cpu_heat_report + "\n" + \
                disk_report)