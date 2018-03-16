from ReinvestClient import ReinvestClient
from util import makeDateObject
import time, schedule, logging, json

data = json.load(open('app_config.json'))
phoneNumber = data["phone-number"]
lastReinvestTime = makeDateObject(data["lastReinvest"], "%d/%m/%Y %H:%M")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename=r"./logs/main.log", filemode="a+",
                        format="%(asctime)s - %(levelname)s - %(message)s")

client = ReinvestClient(data["appSettings"]["api_id"], data["appSettings"]["api_hash"], phoneNumber, lastReinvestTime, schedule)

while True:
    schedule.run_pending()
    time.sleep(1)