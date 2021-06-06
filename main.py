import tweepy


# Authenticate to Twitter
auth = tweepy.OAuthHandler('')


auth.set_access_token('')

# api = tweepy.API(auth)

# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")
    
# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)    

# user = api.get_user("Yohann_matana")

# print("User details:")
# print(user.name)
# print(user.description)
# print(user.location)

# print("últimos 20 seguidores:")
# for follower in user.followers():
#     print(follower.name) 
    
      
# timeline = api.home_timeline()
# for tweet in timeline:
#     print(f"{tweet.user.name} said {tweet.text}")    

    f
api.update_status("teste ^~^")    