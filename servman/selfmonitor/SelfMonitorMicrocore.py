import Battery
import Cpu
import Disk
import re

bad_event_flag = ""
ok_event_flag = ""

def Reporter(bot, adminchatid):
    global bad_event_flag
    global ok_event_flag
    battery_report = Battery.monitor(bot, adminchatid)
    cpu_load_report = Cpu.loadMonitor(bot, adminchatid)
    cpu_heat_report = Cpu.heatMonitor(bot, adminchatid)
    disk_report = Disk.monitor(bot, adminchatid)
    report_list = [battery_report, cpu_load_report, cpu_heat_report, disk_report]
    allow_report = 0
    for report in report_list:
        if report != "" and allow_report == 0:
            print("Report is preparing: " + report)
            allow_report = 1
        

    if allow_report == 1:
        for adminid in adminchatid:
            bot.sendMessage(adminid, battery_report + "\n" + \
                cpu_load_report + "\n" + \
                cpu_heat_report + "\n" + \
                disk_report)