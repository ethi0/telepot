import psutil
import time
import csv

power_flag_s1 = 0
power_flag_s2 = 0
power_plug_flag = 0
power_charge_flag = 0
result_battery = ""


def Monitor():  
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            print("Maybe the power is just [dis]connected." )
            raise AttributeError
        else:
            print("Battery is checked without problems.")
    except AttributeError:
        time.sleep(5)
        battery = psutil.sensors_battery()
        print("Battery is rechecked.")

    batttime = battery.secsleft / 60
    battenergy = battery.percent
    battcharge = battery.power_plugged

    global power_flag_s1
    global power_flag_s2
    global power_plug_flag
    global power_charge_flag
    global result_battery
    if battcharge is False and float(battenergy) > 75.0 and power_flag_s1 == 0:
        power_flag_s1 = 1
        power_flag_s2 = 0
        power_plug_flag = 0
        power_charge_flag = 0
        result_battery = str("[WARNING] Power Unplugged!")
    elif battcharge is False and \
            ((float(batttime) < 75.0 and float(batttime) > 30.0) or (float(battenergy) <= 75.0 and float(battenergy) >= 30.0) and power_flag_s2 == 0):
        power_flag_s1 = 0
        power_flag_s2 = 1
        power_plug_flag = 0
        power_charge_flag = 0
        result_battery = str("[WARNING] Power Unplugged! " + "\n" + \
            "Battery Energy is " + \
            "%.2f percents." % float(battenergy) + "\n" + "%.2f  minutes left!" % float(batttime))
    elif battcharge is False and float(batttime) < 30.0:
        power_flag_s1 = 0
        power_flag_s2 = 0
        power_plug_flag = 0
        power_charge_flag = 0
        result_battery = str("[BAD] Power Unplugged!" + "\n" + \
            "BATTERY CRITICAL: " + \
            "%.2f percents." % float(battenergy) + \
            "\n" + "%.2f minutes left!" % float(batttime))
    elif battcharge is True and float(battenergy) < 100.0 and power_plug_flag == 0:
        power_plug_flag = 1
        power_charge_flag = 0
        power_flag_s1 = 0
        power_flag_s2 = 0
        result_battery = str("[OK] Power Plugged!")
    elif battcharge is True and float(battenergy) == 100.0 and power_charge_flag == 0:
        power_charge_flag = 1
        power_plug_flag = 1
        power_flag_s1 = 0
        power_flag_s2 = 0
        result_battery = str("[OK] Battery is fully charged and on powerline!")
    else:
        result_battery = ""
    return result_battery

    

def Scan():
    battery = psutil.sensors_battery()
    if battery is None:
        return "0"
    elif battery is not None:
        return "1"
    else:
        return "BATTERY,UNDEFINED"
