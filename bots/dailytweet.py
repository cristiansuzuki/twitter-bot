import tweepy
import logging
from config import create_api
import time
import datetime
import random
from datetime import timedelta, datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def daily_tweet(api, last_tweeted, tweets):
    if last_tweeted < datetime.now()-timedelta(hours=24):
        api.update_status(tweets)
        return datetime.now()
    else:
        return last_tweeted
    
def main():
    tweets = ["lobo-guará @Yohann_matana", "flamengo", "tamanduá-bandeira", ".@csuzukib beber água", "bom dia"]
    api = create_api()
    last_tweeted = datetime.now()-timedelta(hours=24)
    while True:
        last_tweeted = daily_tweet(api, last_tweeted, random.choice(tweets))
        logger.info("Waiting...")
        time.sleep(10)
        
if __name__ == "__main__":
    main()        