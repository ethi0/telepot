def addMonitorItem(bot, adminid):
    bot.sendMessage(adminid, "add")
def deleteMonitorItem(bot, adminid):
    bot.sendMessage(adminid, "del")
def editMonitorItem(bot, adminid):
    bot.sendMessage(adminid, "ed")
def listMonitorItems(bot, adminid):
    bot.sendMessage(adminid, "ls")