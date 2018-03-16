import pytz, datetime, logging

def listToString(list, delimiter=","):
    "Helper function to convert a list to a string for logging"
    return delimiter.join(map(str, list))

def getLocalTimezoneOffset():
    "Returns the hours difference between the localtime and UTC"
    "UTC+ return positive hours, UTC- returns negative hours"
    uct_now = pytz.utc.localize(datetime.datetime.utcnow())
    time_now = pytz.utc.localize(datetime.datetime.now())

    return (uct_now-time_now) / datetime.timedelta(hours=1) * -1

def offsetTime(time, hours=0, minutes=0, seconds=0):
    "Accepts datetime object, and offsets by hours/minutes"
    "Returns datetime object"
    return time + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

def calculateLocalReinvestTime(serverTime=None, localTime=None):
    "Calculates the new local time to run reinvest job, accepting the last time of investment ServerTime or Local Time"
    timezoneOffset = getLocalTimezoneOffset()
    offsetHours = 0

    if serverTime:
        # Offset last reinvest time by hours
        #  12 - Reinvest Period
        #  -3 - Server time is UCT+3
        offsetHours = 9 + timezoneOffset
        return offsetTime(serverTime, offsetHours, minutes=1)
    else:
        offsetHours += 12
        return offsetTime(localTime, offsetHours, minutes=1)

def log(messageObj):
    messageObj = str(messageObj)
    print(messageObj)
    logging.info(messageObj)

def makeDateObject(string, format):
    "Returns a datetime object from date and time"
    return datetime.datetime.strptime(string, format)

def makeDateString(date, format):
    "Returns a formatted string from a datetime object"
    return date.strftime(format)

def isReinvestPending(localInvestTime):
    "Compares localInvestTime to the local current time."
    "Returns true if current time is after the calcualted local reinest time"
    time_now = datetime.datetime.now()
    timeDifference = (time_now - localInvestTime) / datetime.timedelta(minutes=1)

    if timeDifference >= 0:
        return True
    else:
        return False