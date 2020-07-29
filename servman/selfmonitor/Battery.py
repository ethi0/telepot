import psutil
import time
from retry import retry

power_flag_s1 = 0
power_flag_s2 = 0
power_plug_flag = 0
power_charge_flag = 0
result_battery = ""


@retry()
def monitor():
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            print("Maybe the power is just [dis]connected. Battery is None == True." )
            raise AttributeError
        else:
            batttime = battery.secsleft / 60
            battenergy = battery.percent
            battcharge = battery.power_plugged
            print("I think it's good there:" + str(battery is None))
    except AttributeError:
        time.sleep(5)
        battery = psutil.sensors_battery()
        print("Action after catching Exception: " + str(battery is None))

    global power_flag_s1
    global power_flag_s2
    global power_plug_flag
    global power_charge_flag
    global result_battery
    if str(battcharge) == str(False) and float(battenergy) > 75.0 and power_flag_s1 == 0:
        power_flag_s1 = 1
        power_flag_s2 = 0
        power_plug_flag = 0
        power_charge_flag = 0
        result_battery = str("[WARNING] Power Unplugged!")
    elif str(battcharge) == str(False) and \
            ((float(batttime) < 75.0 and float(batttime) > 30.0) or (float(battenergy) <= 75.0 and float(battenergy) >= 30.0) and power_flag_s2 == 0):
        power_flag_s1 = 0
        power_flag_s2 = 1
        power_plug_flag = 0
        power_charge_flag = 0
        result_battery = str("[WARNING] Power Unplugged! " + "\n" + \
            "Battery Energy is " + \
            "%.2f percents." % float(battenergy) + "\n" + "%.2f  minutes left!" % float(batttime))
    elif str(battcharge) == str(False) and float(batttime) < 30.0:
        power_flag_s1 = 0
        power_flag_s2 = 0
        power_plug_flag = 0
        power_charge_flag = 0
        result_battery = str("[BAD] Power Unplugged!" + "\n" + \
            "BATTERY CRITICAL: " + \
            "%.2f percents." % float(battenergy) + \
            "\n" + "%.2f minutes left!" % float(batttime))
    elif str(battcharge) == str(True) and float(battenergy) < 100.0 and power_plug_flag == 0:
        power_plug_flag = 1
        power_charge_flag = 0
        power_flag_s1 = 0
        power_flag_s2 = 0
        result_battery = str("[OK] Power Plugged!")
    elif str(battcharge) == str(True) and float(battenergy) == 100.0 and power_charge_flag == 0:
        power_charge_flag = 1
        power_plug_flag = 1
        power_flag_s1 = 0
        power_flag_s2 = 0
        result_battery = str("[OK] Battery is fully charged and on powerline!")
    else:
        result_battery = ""
    return result_battery