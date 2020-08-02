import psutil

def Speed():
    print("In progress...")



def Scan():
    fans = psutil.sensors_fans()
    if fans != {}:
        print("SCAN SAYS: FAN " + str(fans))
        return "1"
    elif fans == {}:
        print("SCAN SAYS2: FAN " + str(fans))
        return "0"
    else:
        return "FANS, UNDEFINED"
