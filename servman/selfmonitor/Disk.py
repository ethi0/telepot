import psutil

def disk_mon(bot, adminchatid):
    disk = psutil.disk_usage('/')
    diskused = disk.percent
    if float(diskused) > 75.0:
        for adminid in adminchatid:
            bot.sendMessage(adminid, "Disk usage is %.2f !" % float(diskused))