from tokens import *
import psutil
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
import operator
import collections
import sys
import time
import threading
import random
import telepot
import socket
import requests
import pymysql
import os

# from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
sys.path.append('./monitor')
import ManageMonItem
import Monitoring
sys.path.append('./scanner')
import Scanner
sys.path.append('./selfmonitor')
import selfMonitorMicrocore
import init

memorythreshold = 85  # If memory usage more this %
poll = 5  # seconds

shellexecution = []
timelist = []
memlist = []
xaxis = []
settingmemth = []
setpolling = []
graphstart = datetime.now()
sysinfo_path = "sysinfo.csv"

stopmarkup = {'keyboard': [['Stop']]}
hide_keyboard = {'hide_keyboard': True}

def clearall(chat_id):
    if chat_id in shellexecution:
        shellexecution.remove(chat_id)
    if chat_id in settingmemth:
        settingmemth.remove(chat_id)
    if chat_id in setpolling:
        setpolling.remove(chat_id)


class YourBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # Do your stuff according to `content_type` ...
        print("Your chat_id:" + str(chat_id)) # this will tell you your chat_id
        if chat_id in adminchatid:  # Store adminchatid variable in tokens.py
            if content_type == 'text':
                if msg['text'] == '/stats' and chat_id not in shellexecution:
                    bot.sendChatAction(chat_id, 'typing')
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    battery = psutil.sensors_battery()
                    cpufreq = psutil.cpu_freq()
                    cpuperc = psutil.cpu_percent()
                    fans = psutil.sensors_fans()
                    temperature = psutil.sensors_temperatures()
                    swap = psutil.swap_memory()
                    loadavg = os.getloadavg()
                    boottime = datetime.fromtimestamp(psutil.boot_time())
                    now = datetime.now()
                    timedif = "Online for: %.2f Hours" % (((now - boottime).total_seconds()) / 3600)
                    memtotal = "Total memory: %.3f GB " % (memory.total / 1000000000)
                    memavail = "Available memory: %.3f GB" % (memory.available / 1000000000)
                    memuseperc = "Used memory: " + str(memory.percent) + " %"
                    diskused = "Disk used: " + str(disk.percent) + " %"
                    battenergy = "Battery energy: %.2f percents" % battery.percent
                    battcharge = "Battery charging: " + str(battery.power_plugged)
                    batttime = "Battery time left: %.2f minutes" % (battery.secsleft / 60)
                    cpuperccurr = "CPU Load " + str(cpuperc.conjugate()) + " %"
                    cpurfreqcurr = "CPU frequency: %.2f MHz" % cpufreq.current
                    cputemp = "CPU Temperature " + str(temperature.get('coretemp')[0][1])
                    fanscurr = "FAN RPM " + str(fans.get('dell_smm')[0][1])
                    swapused = "SWAP used " + str(swap.used / 1024 / 1024) + " MB"
                    loadavgcurr = "Load AVG " + str(loadavg)
                    pids = psutil.pids()
                    pidsreply = ''
                    procs = {}
                    for pid in pids:
                        p = psutil.Process(pid)
                        try:
                            pmem = p.memory_percent()
                            if pmem > 0.5:
                                if p.name() in procs:
                                    procs[p.name()] += pmem
                                else:
                                    procs[p.name()] = pmem
                        except:
                            print("Hm")
                    sortedprocs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
                    for proc in sortedprocs:
                        pidsreply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"
                    reply = timedif + "\n" + \
                            memtotal + "\n" + \
                            memavail + "\n" + \
                            memuseperc + "\n" + \
                            diskused + "\n" + \
                            battenergy + "\n" + \
                            battcharge + "\n" + \
                            batttime + "\n" + \
                            loadavgcurr + "\n" + \
                            cpuperccurr + "\n" + \
                            cpurfreqcurr + "\n" + \
                            cputemp + "\n" + \
                            fanscurr + "\n" + \
                            swapused + "\n\n" + \
                            pidsreply
                    bot.sendMessage(chat_id, reply, disable_web_page_preview=True)
                elif msg['text'] == "Stop":
                    clearall(chat_id)
                    bot.sendMessage(chat_id, "All operations stopped.", reply_markup=hide_keyboard)
                elif msg['text'] == "/shell" and chat_id not in shellexecution:
                    bot.sendMessage(chat_id, "Send me a shell command to execute", reply_markup=stopmarkup)
                    shellexecution.append(chat_id)
                elif msg['text'] == "/madd" and chat_id not in shellexecution:
                    ManageMonItem.addMonitorItem(bot, chat_id)
                elif msg['text'] == "/mdel" and chat_id not in shellexecution:
                    ManageMonItem.deleteMonitorItem(bot, chat_id)
                elif msg['text'] == "/medit" and chat_id not in shellexecution:
                    ManageMonItem.editMonitorItem(bot, chat_id)
                elif msg['text'] == "/mstart" and chat_id not in shellexecution:
                    Monitoring.startMonitorItems(bot, chat_id)
                elif msg['text'] == "/mstop" and chat_id not in shellexecution:
                    Monitoring.stopMonitorItems(bot, chat_id)
                elif msg['text'] == "/sscan" and chat_id not in shellexecution:
                    Scanner.startScanItem(bot, chat_id)
                elif chat_id in shellexecution:
                    bot.sendChatAction(chat_id, 'typing')
                    p = Popen(msg['text'], shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                    output = p.stdout.read()
                    if output != b'':
                        bot.sendMessage(chat_id, output, disable_web_page_preview=True)
                    else:
                        bot.sendMessage(chat_id, "No output.", disable_web_page_preview=True)


TOKEN = telegrambot

bot = YourBot(TOKEN)
bot.message_loop()
tr = 0
xx = 0
for adminid in adminchatid:
    bot.sendMessage(adminid, "ALL SYSTEMS ARE ONLINE." + "\n" \
        + "Initializing first-time check...")
init.Scan(bot, adminchatid, sysinfo_path)
selfMonitorMicrocore.Reporter(bot, adminchatid, sysinfo_path)
# Keep the program running.
while 1:
    if tr == poll:
        tr = 0
        timenow = datetime.now()
        memck = psutil.virtual_memory()
        mempercent = memck.percent
        selfMonitorMicrocore.Reporter(bot, adminchatid, sysinfo_path)
        if len(memlist) > 300:
            memq = collections.deque(memlist)
            memq.append(mempercent)
            memq.popleft()
            memlist = memq
            memlist = list(memlist)
        else:
            xaxis.append(xx)
            xx += 1
            memlist.append(mempercent)
        memfree = memck.available / 1000000
        if mempercent > memorythreshold:
            memavail = "Available memory: %.2f GB" % (memck.available / 1000000000)
            graphend = datetime.now()
            tmperiod = "Last %.2f hours" % ((graphend - graphstart).total_seconds() / 3600)
            for adminid in adminchatid:
                bot.sendMessage(adminid, "CRITICAL! LOW MEMORY!\n" + memavail)
    time.sleep(5)  # 10 seconds
    tr += 5