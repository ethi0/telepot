import Battery
import Cpu
import Disk


def Reporter(bot, adminchatid):
    battery_report = Battery.monitor()
    cpu_load_report = Cpu.loadMonitor()
    cpu_heat_report = Cpu.heatMonitor()
    disk_report = Disk.monitor()
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