import psutil

def Speed():
    print("In progress...")
    


def Scan():
    fans = psutil.sensors_fans()
    if fans is None:
        return "0"
    elif fans is not None:
        return "1"
    else:
        return "FANS, UNDEFINED"
