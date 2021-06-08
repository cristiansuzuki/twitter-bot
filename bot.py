import tweepy
import os
import logging
import time
import datetime
import random
from datetime import timedelta, datetime
import dotenv
from dotenv import load_dotenv

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
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

create_api()

# Checa se possui novos seguidores, se sim, o bot segue o usuário de volta.
def follow_followers(api):
    logger.info("Verificando seguidores e seguindo de volta...")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Seguindo {follower.name}")
            follower.follow()

# Checa as mentions pra ver se alguem mencionou o bot...
def check_mentions(api, keywords, since_id):
    logger.info("Recuperando mentions...")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Respondendo {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                ("@" + tweet.user.screen_name + " " + "salve ^~^"),
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

# Função que poste tweets diários (no caso abaixo, a cada 12 horas)
def daily_tweet(api, last_tweeted, tweets):
    logger.info("Daily tweet (?)")
    if last_tweeted < datetime.now()-timedelta(hours=12):
        api.update_status(tweets)
        return datetime.now()
    else:
        return last_tweeted
    
# Função que curte e retweeta tweets onde possuem a hashtag #redzinbot
def like(api):
    search = '#redzinbot'
    limit = 5
    
    for tweet in tweepy.Cursor(api.search, search).items(limit):
        try:
            print('Tweet curtido e retweetado...')
            tweet.favorite()
            tweet.retweet()
            time.sleep(10)
        except Exception as e:
            logger.error("Error on fav", exc_info=True)       

# Função que tweeta novos tweets do Woj da ESPN (insider NBA) - Ainda em construção
# def woj():
#     api = create_api()
#     tweets_woj = api.user_timeline(screen_name="wojespn",
#                     # 200 is the maximum allowed count
#                     count=100,
#                     include_rts = False,
#                     # Necessary to keep full_text 
#                     # otherwise only the first 140 words are extracted
#                     tweet_mode = 'extended'
#                     )
#     for info in tweets_woj[:5]:
#             if info.in_reply_to_status_id is None:
#                 # Tweet is a reply
#                 try:
#                     logger.info("Postando tweets do Woj...")
#                     api.update_status(status = info.full_text)
#                 except:
#                     return
#                     # Tweet is not a reply 
    
def main():
    since_id = 1
    tweets = ["lobo-guará @Yohann_matana", "flamengo", "tamanduá-bandeira", ".@csuzukib beber água", "bom dia", 
              ".@Williammaffii vai treinar mlk horrível ^~^",
              "ç.ç",
              "Porque se botar você de IGL na Astralis, ele vai olhar dentro da tua cara, filha da puta, e vai te convencer a você pensar que você é o Gla1ve, e você vai dar uma call pra ele e ele vai meter 1vs 5 no clutch e vai te dar duzentos-mil-réis. Porque é assim, entendeu, cara?",
              "xd",
              "ntc ^~^",
              ".@csuzukib to em choque",
              ".@elonmusk send salve",
              ".@rodrigomcc Aqui vai um vídeo para você https://www.youtube.com/watch?v=WMZNLy0hGEI&ab_channel=IntegrandoConhecimento",
              "https://www.youtube.com/watch?v=nfUdAaPgbo0&ab_channel=geezluis99geezluis99",
              "https://www.youtube.com/watch?v=F2DrEBIG5-E&ab_channel=GQSports",
              "hj é sexta-feira",
              ".@kingjames the GOAT",
              "boa noite randoms",
              "O_o https://www.youtube.com/watch?v=eUOYCXymFWE&ab_channel=slater%21slater%21",
              ";D",
              "Carl Edward Sagan foi um cientista, físico, biólogo, astrônomo, astrofísico, cosmólogo, escritor, divulgador científico e ativista norte-americano.",
              ".@indigitalvoid ~_~",
              "Se hoje for terça-feira, o mundo é uma simulação.",
              "Infelizmente acabou a competitividade, não existe mais nenhum adversário a altura do Celtics na América do Norte. Está na hora do Celtics ir pra Europa e jogar a Euroliga, ou em uma jogada mais ousada, se filiar a FIBA como uma seleção e disputar a copa do Qatar 2022",
              "Em caso de investigação policial, eu oficialmente declaro que não tenho envolvimento com este grupo, provavelmente fui inserido por terceiros, estou disposto a colaborar com as investigações e a me apresentar a depoimento se necessário, sou completamente inocente.",
              "Se as pessoas soubessem o que aconteceu na Flashpoint 2020, ficariam enojadas.",
              "ih 🥴 🥴 🥴 pressao baixo 🤒 🤒 🤒 🤒 ih 🥱 🥱 🥱 🥴 pressao baixo 🥱 🤒 🤒 👎 zzzzZZZZZZ 😴 😴 😴 zzzZZZZZZZ 😴 😴 😴 😴 😴 zzzzZZZZZZ 😴 😴 😴 zzzZZZZZZZ 😴 😴 😴 😴 😴 salve ai mano 😜 👍",
              ".@TheusSuzuki la vai o pix O_______O",
              "coisas toscas que me irritam: memes sobre sobre como o pessoal do ratatouille ia pegar intoxicação alimentar vocês não assistiram o filme, seus cornos filhos da pu7a? O REMI NÃO TOCA NA COMIDA. ele fica puxando o cabelo da passiva lá e ELA mexe na comida.",
              "ONDE CARALHOS ESTÃO OS OUTROS 2076 CYBERPUNKS?",
              "maldito seja o asteroide que se fragmentou e formou o meteoro que caiu sobre a terra, dizimando os animais que viraram fósseis e depois petróleo que foi extraído e usado na fabricação do combustível, que abasteceu o carro de cimento pra fazer o hospital que você nasceu",
              "Pra jogar CS, você não precisa de um pênis. Tudo que você precisa é um teclado, um mouse, uma conexão ADSL, ter o jogo instalado e um pouco de talento. Não distrate mulheres que jogam CS, elas são raras. @williammaffi @yohann_matana",
              ".@estrogonofre2 é ruim ? Qual foi a ultima vez que você viu um jogador ter esse controle de mira e spray ? Nós seremos abençoados se vermos um jogador com as suas habilidades e paixão de novo. S1mple quebra recordes, ZyWoo quebra recordes. Faboka quebra as regras."
              
              ]
    api = create_api()
    last_tweeted = datetime.now()#-timedelta(hours=12)
    while True:
        like(api)
        follow_followers(api)
        since_id = check_mentions(api, ["salve", "e ai", "oi", ""], since_id)
        last_tweeted = daily_tweet(api, last_tweeted, random.choice(tweets))
        # woj()
        logger.info("Esperando timer...")
        time.sleep(60)
        
if __name__ == "__main__":
    main()        