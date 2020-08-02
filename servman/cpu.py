import psutil
import os

low_heat_flag = 0
high_heat_flag = 0
low_load_flag = 0
high_load_flag = 0
result_heat = ""
result_load = ""

def heatMonitor():
    global low_heat_flag
    global high_heat_flag
    global result_heat
    temperature = psutil.sensors_temperatures()
    cputemp = list(temperature.values())[0][0][1]
    if float(cputemp) > 60.0 and high_heat_flag == 0:
        high_heat_flag = 1
        low_heat_flag = 0
        result_heat = str("[BAD] CPU Temperature is %.2f degrees!" % float(cputemp))
    elif float(cputemp) < 60.0 and low_heat_flag == 0:
        high_heat_flag = 0
        low_heat_flag = 1
        result_heat = str("[OK] CPU Temperature is %.2f degrees!" %float(cputemp))
    else:
        result_heat = ""
    return result_heat




def loadMonitor():
    global low_load_flag
    global high_load_flag
    global result_load
    loadavg = os.getloadavg()
    if int(loadavg[0]) > 4 and int(loadavg[1]) > 4 and high_load_flag == 0:
        high_load_flag = 1
        low_load_flag = 0
        result_load = str("[BAD] Load is HIGH!" + \
            "%.2f, %.2f, %.2f" % (float(loadavg[0]), float(loadavg[1]), float(loadavg[2])))
    elif int(loadavg[0]) < 4 and int(loadavg[1]) < 4 and low_load_flag == 0:
        high_load_flag = 0
        low_load_flag = 1
        result_load = str("[OK] Load is normal." + \
            "%.2f, %.2f, %.2f" % (float(loadavg[0]), float(loadavg[1]), float(loadavg[2])))
    else:
        result_load = ""
    return result_load


def Scan():
    return str(psutil.cpu_count())