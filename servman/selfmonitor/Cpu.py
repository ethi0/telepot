import psutil

def cpu_mon(bot, adminchatid):
    temperature = psutil.sensors_temperatures()
    cputemp = temperature.get('coretemp')[0][1]
    if float(cputemp) > 70.0:
        for adminid in adminchatid:
            bot.sendMessage(adminid, "CPU Temperature is %.2f !" % float(cputemp))
