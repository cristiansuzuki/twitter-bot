import tweepy
import os
import logging
import time
import datetime
import random
from datetime import timedelta, datetime
import dotenv
from dotenv import load_dotenv
import requests
import json
import urllib.request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from dotenv import load_dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

logger = logging.getLogger()

# Função para autenticar a API. Deve ter um arquivo .env na raiz com as suas variáveis e chaves definidas.
def create_api():
    consumer_key = os.getenv("consumer_key")
    consumer_secret = os.getenv("consumer_secret")
    access_token = os.getenv("access_token")
    access_token_secret = os.getenv("access_token_secret")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=False, compression=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


# Checa se possui novos seguidores, se sim, o bot segue o usuário de volta.
def follow_followers(api):
    logger.info("Verificando seguidores e seguindo de volta...")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            if follower.protected==False:
                logger.info(f"Seguindo {follower.name}")
                follower.follow()
            else:
                logger.info("usuário com a conta fechada")
                pass
        else:
            # logger.info("Nenhum seguidor novo...")
            pass
        
def daily_tweet(api, last_tweeted):
    numero = str(random.randint(1, 898)) 
    URL = "https://pokeapi.co/api/v2/pokemon/" + numero +"/"
    try:
        response = requests.get(URL)
    except:
        logger.info("Erro ao chamar API...")

    res = json.loads(response.text)
    
    id_pokemon = str(res['id'])
    nome_pokemon = res['name']
    imagem_pokemon = res['sprites']['other']['home']['front_default'] 

    with urllib.request.urlopen(imagem_pokemon) as url:
        with open('temp.jpg', 'wb') as f:
            f.write(url.read())
    
    media = api.media_upload("temp.jpg")
    tweet = 'ID: ' + str(id_pokemon) + '\nNome: ' + nome_pokemon
        
    with open('ids.txt') as f:
        ids = f.readlines()
        lista=[]
        for i in range(len(ids)):
            lista.append(int(ids[i]))
            
    id_pokemon_int = int(id_pokemon)
    
    if id_pokemon_int in lista:
        logger.info('Este pokémon já foi publicado.')
        pass
    else:
        if last_tweeted < datetime.now()-timedelta(hours=12):
            api.update_status(status=tweet, media_ids=[media.media_id])
            with open('ids.txt', 'a') as f:
                f.write(id_pokemon)
                f.write('\n')
            logger.info('Pokemon publicado com sucesso !')        
            return datetime.now()
        else:
            logger.info('Não é hora de publicar...')
            return last_tweeted
        
def main(api):         
    # numero = str(random.randint(1, 898)) 
    
    # URL = "https://pokeapi.co/api/v2/pokemon/" + numero +"/"
    # try:
    #     response = requests.get(URL)
    # except:
    #     logger.info("Erro ao chamar API...")

    # res = json.loads(response.text)
    
    # id_pokemon = str(134)
    # nome_pokemon = res['name']
    # imagem_pokemon = res['sprites']['front_default']
    
    
    # with urllib.request.urlopen(imagem_pokemon) as url:
    #     with open('temp.jpg', 'wb') as f:
    #         f.write(url.read())
    
    # media = api.media_upload("temp.jpg")
    # tweet = 'ID: ' + str(id_pokemon) + '\nNome: ' + nome_pokemon
        
    # with open('ids.txt') as f:
    #     ids = f.readlines()
    #     lista=[]
    #     for i in range(len(ids)):
    #         lista.append(int(ids[i]))
            
    # id_pokemon_int = int(id_pokemon)
    
    # if id_pokemon_int in lista:
    #     logger.info('Este pokémon já foi publicado.')
    #     pass
    # else:
    #     logger.info('teste...')
    #     media, tweet, id_pokemon

    last_tweeted = datetime.now()#-timedelta(hours=12)
    while True:
        # like(api)
        follow_followers(api)
        last_tweeted = daily_tweet(api, last_tweeted)
        logger.info("Esperando timer...")
        time.sleep(60)
        
if __name__ == "__main__":
    main(create_api())      

