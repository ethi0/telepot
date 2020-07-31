import psutil

disk_full_flag = 0
disk_free_flag = 0
result_disk = ""

def Monitor():
    global disk_free_flag
    global disk_full_flag
    global result_disk
    disk = psutil.disk_usage('/')
    diskused = disk.percent
    if float(diskused) > 75.0 and disk_full_flag == 0:
        disk_full_flag = 1
        disk_free_flag = 0
        result_disk = str("[BAD] Disk usage is %.2f percents!" % float(diskused))
    elif float(diskused) < 75.0 and disk_free_flag == 0:
        disk_full_flag = 0
        disk_free_flag = 1
        result_disk = str("[OK] Disk usage is %.2f percents!" % float(diskused))
    else:
        result_disk = ""
    return result_disk