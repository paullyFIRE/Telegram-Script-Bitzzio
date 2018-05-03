# Bitzz.io Telegram Reinvest Script

Hey.

This is a basic script written in Python 3 to re-invest max available balance with the Bitzzio telegram bot.

Since the Bitzzio Program has officially closed, here is some context to this project:

Bitzzio was a HYIP within the crypto-space that allowed effective compounding every 12 hours. 
This was either done manually through the dashboard, or by sending the message '/reinvest max' to a telegram-bot that is linked to the online dashboard. 
While the telegram bot for the program is convenient, it is not so when the next possible reinvest (compound) should be triggered at 3am.

Cue script.

For maximum continuous compounding, the message was to be send to the telegram bot every 12 hours. 
This script was written taking the last investment timestamp, and then calculating the next possible opportunity. 
If it passed, it automatically send the message to the telegram bot and then schedueled itself to so again after 12 hours. 
Else, if there is no opportunity to reinvest yet according to the timestamp, 
it'll schedule to send the message at the next opportunity, and then re-schedule to do the same every 12 hours thereafter.

## How the script schedules re-investing

When the script is run, it sets up regular 12 hour reinvest cycles in the following way:

    1. It first takes the last reinvest date and time, and then calculates when to next reinvest after 12 hours, in your local time.
    2. It will then schedule to run the first reinvest when that time comes. 
       Depending on your local time relative to the next Reinvest time, the script will do two things:
        2.1 If your local time is before the 12 hour reinvest point of the last reinvestment, it will simply wait until it's time to reinvest.
        2.2 If your localtime has passed the 12 hour reinvest point of the last reinvestment, it will instantly send the first reinvest message to the Bitzzio bot.
    3. After the first reinvest, it will send the message to the Bitzzio telegram bot "/reinvest max", to reinvest your available balance at the time.
    4. Once reinvested, it will set up a recurring schedule for every 12 hours, to repeat the re-invest. This will continue until the script is stopped.

## To configure it for your use, you need to configure the following details:

    Last Reinvest Time: This is the last time you reinvested. It'll be the bottom-most deposit entry in the dashboard.
        Format is DD/MM/YYYY HH:MM.
        E.g Last reinvest was 15 March 2018 15:42 - then this should be "15/03/2018 15:42".
    Phone Number: 
        This is your telegram profile's phone number, internationally formatted with your country code.
        A South African (+27) number 079-587-6686 will become +27795876686 (drop the leading 0)
    API_ID and API_HASH:
        You can get these from https://my.telegram.org/auth.
        Log in with your telegram mobile number (this number will work within the script's settings file)
        Once logged in, go to 'API development tools'.
        Create a new app, where you'll get your App api_id and App api_hash.

## To install the local environment needed to run the script:

    1. Install Python 3.5+ (https://www.python.org/downloads/)
    2. Insure to add Python to your PATH environment on setup.
    3. Once installed, you should be able to open a CMD console, and typing 'Python --version' should return the install version.
    4. Now that Python is setup, we need to install the script's dependencies.
       You can do this quickly by typing this into the CMD console: 'pip install telethon schedule pytz'
    5. That's the setup completed. Ensure you have added your settings to the app_config.json.EXAMPLE file (open it in wordpad or preferred editor.), and then remove the '.EXAMPLE' suffix.
    6. To run the app, in a CMD console type 'python bitz-reinvest-bot.py'

Provided that your number is correctly formatted, you'll be prompted to enter a passcode that is sent to your telegram client/mobile phone.
Once authenticated, you'll be automatically be logged in next time your run the script.

If you need any assistance, hit me up on telegram @paullyFIRE, or by email at pddpatterson@gmail.com.

Suggestions and critique welcome.
