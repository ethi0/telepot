import psutil
import os

heat_flag = 0
load_flag = 0


def heatMonitor(bot, adminchatid):
    global heat_flag
    temperature = psutil.sensors_temperatures()
    cputemp = temperature.get('coretemp')[0][1]
    if float(cputemp) > 70.0:
        for adminid in adminchatid:
            bot.sendMessage(adminid, "CPU Temperature is %.2f !" %
                            float(cputemp))


def loadMonitor(bot, adminchatid):
    global load_flag
    loadavg = os.getloadavg()
    if int(loadavg[0]) > 4 and int(loadavg[1]) > 4 and load_flag == 0:
        load_flag = 1
        for adminid in adminchatid:
            bot.sendMessage(adminid, "Load is HIGH!" + "\n" +
                "%.2f, %.2f, %.2f" % float(loadavg[0]) % float(loadavg[1]) % float(loadavg[2]))
    elif int(loadavg[0]) < 4 and int(loadavg[1]) < 4 and load_flag == 1:
        load_flag = 0
        for adminid in adminchatid:
            bot.sendMessage(adminid, "Load is normal." + "\n" +
                "%.2f, %.2f, %.2f" % float(loadavg[0]) % float(loadavg[1]) % float(loadavg[2]))
