import psutil

power_flag_s1 = 0
power_flag_s2 = 0
power_plug_flag = 0
power_charge_flag = 0

def monitor(bot, adminchatid):
    battery = psutil.sensors_battery()
    battenergy = battery.percent
    battcharge = battery.power_plugged
    batttime = battery.secsleft / 60
    global power_flag_s1
    global power_flag_s2
    global power_plug_flag
    global power_charge_flag
    if str(battcharge) == str(False) and float(battenergy) > 75.0:
        if power_flag_s1 == 0:
            power_flag_s1 = 1
            power_flag_s2 = 0
            power_plug_flag = 0
            for adminid in adminchatid:
                bot.sendMessage(adminid, "Power Unplugged!")
    elif str(battcharge) == str(False) and \
            ((float(batttime) < 75.0 and float(batttime) > 30.0) or (float(battenergy) <= 75.0 and float(battenergy) >= 30.0)):
        if power_flag_s2 == 0:
            power_flag_s1 = 0
            power_flag_s2 = 1
            power_plug_flag = 0
            for adminid in adminchatid:
                bot.sendMessage(adminid, "Power Unplugged! " + "\n" +
                    "Battery Energy is "
                    + "%.2f percents." % float(battenergy) + "\n" + "%.2f  minutes left!" % float(batttime))
    elif str(battcharge) == str(False) and float(batttime) < 30.0:
        power_flag_s1 = 0
        power_flag_s2 = 0
        power_plug_flag = 0
        for adminid in adminchatid:
            bot.sendMessage(adminid, "Power Unplugged!" + "\n" +
                "BATTERY CRITICAL: " +
                "%.2f percents." % float(battenergy)
                + "\n" + "%.2f minutes left!" % float(batttime))
    elif str(battcharge) == str(True) and float(battenergy) < 100.0 and power_plug_flag == 0:
        power_plug_flag = 1
        power_charge_flag = 0
        for adminid in adminchatid:
            bot.sendMessage(adminid, "Power Plugged!")
    elif str(battcharge) == str(True) and float(battenergy) == 100.0 and power_charge_flag == 0:
        power_charge_flag = 1
        for adminid in adminchatid:
            bot.sendMessage(
                adminid, "Battery is fully charged and on powerline!")
