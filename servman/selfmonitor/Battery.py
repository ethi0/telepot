import psutil

power_flag_s1 = 0
power_flag_s2 = 0
power_plug_flag = 0
power_charge_flag = 0
result_battery = ""

def monitor(bot, adminchatid):
    battery = psutil.sensors_battery()
    battcharge = battery.power_plugged
    batttime = battery.secsleft / 60
    while True:
        try:
            battenergy = battery.percent
        except AttributeError:
            for adminid in adminchatid:
                bot.sendMessage(adminid, "[ERROR] There is an error while getting battery.percent value! Retrying...")
        break
    
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
        result_battery = str("[BAD] Power Unplugged!" + "\n" + \
            "BATTERY CRITICAL: " + \
            "%.2f percents." % float(battenergy) + \
            "\n" + "%.2f minutes left!" % float(batttime))
    elif str(battcharge) == str(True) and float(battenergy) < 100.0 and power_plug_flag == 0:
        power_plug_flag = 1
        power_charge_flag = 0
        result_battery = str("[OK] Power Plugged!")
    elif str(battcharge) == str(True) and float(battenergy) == 100.0 and power_charge_flag == 0:
        power_charge_flag = 1
        result_battery = str("[OK] Battery is fully charged and on powerline!")
    else:
        result_battery = ""
    return result_battery
