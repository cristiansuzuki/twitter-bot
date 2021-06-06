import tweepy
import logging
from config import create_api
import time

api = create_api()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

tweets_home = api.home_timeline(count=100)

def like(api):
    for tweet in tweets_home:
        if tweet.author.name.lower() == "red":
            if not tweet.favorited:
                # Mark it as Liked, since we have not done it yet
                try:
                    tweet.favorite()
                except Exception as e:
                    logger.error("Error on fav", exc_info=True)
            
def main():
    while True:
        like(api)
        logger.info("Waiting...")
        time.sleep(10)
            
if __name__ == "__main__":
    main()            
            