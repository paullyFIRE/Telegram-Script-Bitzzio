from telethon import TelegramClient
from util import log, calculateLocalReinvestTime, isReinvestPending, makeDateString, makeDateObject
import hashlib, datetime

class ReinvestClient:
    scheduleJobFormat = "%H:%M"
    logJobFormat = "%H:%M %d/%m/%Y"
    botChannel = "bitzziobot"

    def __init__(self, api_id, api_hash, phoneNumber, investTime, schedule):
        # App Settings
        self.api_id = api_id
        self.api_hash = api_hash
        self.phoneNumber = phoneNumber
        # Datetime object of last reinvestment
        self.lastReinvestServerTime = investTime
        # Schedule variables for job runs
        self.schedule = schedule
        self.scheduleJob = None
        # Telegram authentication boolean
        self.isAuthed = False
        
        self.authenticateClient()

        # check auth conditional for future login-handlers
        if (self.isAuthed):
            self.initSchedule()

    def authenticateClient(self):
        "Checks if authenticated to Telegram, initiates Auth if not"
        client = self.initClient()
        client.connect()

        if not client.is_user_authorized():
            client.send_code_request(self.phoneNumber)
            client.sign_in(self.phoneNumber, input("Enter code: "))
            # Add error handling for failed auth attempts
            self.isAuthed = True
        else:
            # Already authenticated
            self.isAuthed = True

        log("Welcome. You've successfully logged in as " + client.get_me().username)

        client.disconnect()

    def initSchedule(self):
        "Initializes the first scheduled job for first reinvest"
        # Datetime object of next local invest time
        localInvestTime = calculateLocalReinvestTime(serverTime=self.lastReinvestServerTime)

        # self.localInvestTime = makeDateObject("16/03/2018 07:17", "%d/%m/%Y %H:%M")
        log("You last reinvested @ " + makeDateString(self.lastReinvestServerTime, self.logJobFormat))
        
        # Checks if a reinvest is overdue since last reinvest
        if isReinvestPending(localInvestTime):
            log("It's been move than 12 hours since last reinvest. Reinvesting...")

            self.reinvestJobCycle()
        else:
            investTimeStr = makeDateString(localInvestTime, self.scheduleJobFormat)
            self.scheduleJob = self.schedule.every().day.at(investTimeStr).do(self.reinvestJobCycle)

            log("First reinvest scheduled for " + makeDateString(localInvestTime, self.logJobFormat))

    def reinvestJobCycle(self):
        "Cancels current job, instantiates the next 43201 (12 hour) cycle to reinvest"
        lastReinvestTime = self.reinvest()
        nextLocalInvestTime = calculateLocalReinvestTime(localTime=lastReinvestTime)

        self.schedule.cancel_job(self.scheduleJob)
        self.scheduleJob = self.schedule.every().day.at(makeDateString(nextLocalInvestTime, self.scheduleJobFormat)).do(self.reinvestJobCycle)

        log("Next reinvest will happen @ " + makeDateString(nextLocalInvestTime, self.logJobFormat))

    def initClient(self):
        "instantiates a new client instance"
        # MD5 hash used for unique client-specific identifiers
        phoneHash = hashlib.md5((self.phoneNumber).encode('utf-8')).hexdigest()

        client = TelegramClient("./sessions/" + phoneHash + ".session", self.api_id, self.api_hash, update_workers=1, spawn_read_thread=False)
        return client

    def reinvest(self):
        "Starts new session with telegram and sends reinvest message to bot"
        client = self.initClient()
        client.start()
        client.send_message(self.botChannel, "/reinvest max")
        localReinvestTime = datetime.datetime.now()

        log("Sent Reinvest Message to " + self.botChannel + "  - " + makeDateString(localReinvestTime, self.logJobFormat))

        client.disconnect()
        return localReinvestTime

    def getScheduleJobs(self):
        "Get method for client's active jobs"
        return self.schedule.jobs

