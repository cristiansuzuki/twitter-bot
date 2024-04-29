import tweepy
import os
import logging
import time
import datetime
import random
from datetime import timedelta, datetime, date
import dotenv
from dotenv import load_dotenv
import requests
import json
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats import endpoints
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


dotenv.load_dotenv(dotenv.find_dotenv())

logger = logging.getLogger()




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
            if follower.protected == False:
                logger.info(f"Seguindo {follower.name}")
                follower.follow()
            else:
                logger.info("usuário com a conta fechada")
                pass
        else:
            # logger.info("Nenhum seguidor novo...")
            pass


def daily_tweet(api):

    ####################################### PLAYOFFS !!! #################################################################

    # Lideres totais em pontos nos playoffs
    data_pontos_playoffs = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, season_type_all_star='Playoffs')
    df_pontos_playoffs = data_pontos_playoffs.league_leaders.get_data_frame()
    pontos_totais_playoffs = 'NBA - Top 5 Playoffs 2022: Pontos totais ' + '\n' + '\n' + str(df_pontos_playoffs.PLAYER[0]) + ' - ' + str(df_pontos_playoffs.PTS[0]) + ' pontos' + '\n' + str(df_pontos_playoffs.PLAYER[1]) + ' - ' + str(df_pontos_playoffs.PTS[1]) + ' pontos' + '\n' + str(
        df_pontos_playoffs.PLAYER[2]) + ' - ' + str(df_pontos_playoffs.PTS[2]) + ' pontos' + '\n' + str(df_pontos_playoffs.PLAYER[3]) + ' - ' + str(df_pontos_playoffs.PTS[3]) + ' pontos' + '\n' + str(df_pontos_playoffs.PLAYER[4]) + ' - ' + str(df_pontos_playoffs.PTS[4]) + ' pontos'

    # Lideres em rebotes totais nos playoffs
    data_rebotes_playoffs = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, stat_category_abbreviation='REB', season_type_all_star='Playoffs')
    df_rebotes_playoffs = data_rebotes_playoffs.league_leaders.get_data_frame()
    rebotes_totais_playoffs = 'NBA - Top 5 Playoffs 2022: Rebotes totais' + '\n' + '\n' + str(df_rebotes_playoffs.PLAYER[0]) + ' - ' + str(df_rebotes_playoffs.REB[0]) + ' rebotes' + '\n' + str(df_rebotes_playoffs.PLAYER[1]) + ' - ' + str(df_rebotes_playoffs.REB[1]) + ' rebotes' + '\n' + str(
        df_rebotes_playoffs.PLAYER[2]) + ' - ' + str(df_rebotes_playoffs.REB[2]) + ' rebotes' + '\n' + str(df_rebotes_playoffs.PLAYER[3]) + ' - ' + str(df_rebotes_playoffs.REB[3]) + ' rebotes' + '\n' + str(df_rebotes_playoffs.PLAYER[4]) + ' - ' + str(df_rebotes_playoffs.REB[4]) + ' rebotes'

    # Lideres em assistencias totais nos playoffs
    data_assistencias_playoffs = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, stat_category_abbreviation='AST', season_type_all_star='Playoffs')
    df_assistencias_playoffs = data_assistencias_playoffs.league_leaders.get_data_frame()
    assistencias_totais_playoffs = 'NBA - Top 5 Playoffs 2022: Assistencias totais' + '\n' + '\n' + str(df_assistencias_playoffs.PLAYER[0]) + ' - ' + str(df_assistencias_playoffs.AST[0]) + ' assistencias' + '\n' + str(df_assistencias_playoffs.PLAYER[1]) + ' - ' + str(df_assistencias_playoffs.AST[1]) + ' assistencias' + '\n' + str(
        df_assistencias_playoffs.PLAYER[2]) + ' - ' + str(df_assistencias_playoffs.AST[2]) + ' assistencias' + '\n' + str(df_assistencias_playoffs.PLAYER[3]) + ' - ' + str(df_assistencias_playoffs.AST[3]) + ' assistencias' + '\n' + str(df_assistencias_playoffs.PLAYER[4]) + ' - ' + str(df_assistencias_playoffs.AST[4]) + ' assistencias'

    # Lideres em roubos de tola totais nos playoffs
    data_roubos_playoffs = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, stat_category_abbreviation='STL', season_type_all_star='Playoffs')
    df_roubos_playoffs = data_roubos_playoffs.league_leaders.get_data_frame()
    roubos_totais_playoffs = 'NBA - Top 5 Playoffs 2022: Roubos de bola totais' + '\n' + '\n' + str(df_roubos_playoffs.PLAYER[0]) + ' - ' + str(df_roubos_playoffs.STL[0]) + ' roubos' + '\n' + str(df_roubos_playoffs.PLAYER[1]) + ' - ' + str(df_roubos_playoffs.STL[1]) + ' roubos' + '\n' + str(
        df_roubos_playoffs.PLAYER[2]) + ' - ' + str(df_roubos_playoffs.STL[2]) + ' roubos' + '\n' + str(df_roubos_playoffs.PLAYER[3]) + ' - ' + str(df_roubos_playoffs.STL[3]) + ' roubos' + '\n' + str(df_roubos_playoffs.PLAYER[4]) + ' - ' + str(df_roubos_playoffs.STL[4]) + ' roubos'

    # Lideres em tocos totais nos playoffs
    data_tocos_playoffs = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, stat_category_abbreviation='BLK', season_type_all_star='Playoffs')
    df_tocos_playoffs = data_tocos_playoffs.league_leaders.get_data_frame()
    tocos_totais_playoffs = 'NBA - Top 5 Playoffs 2022: Tocos totais' + '\n' + '\n' + str(df_tocos_playoffs.PLAYER[0]) + ' - ' + str(df_tocos_playoffs.BLK[0]) + ' tocos' + '\n' + str(df_tocos_playoffs.PLAYER[1]) + ' - ' + str(df_tocos_playoffs.BLK[1]) + ' tocos' + '\n' + str(
        df_tocos_playoffs.PLAYER[2]) + ' - ' + str(df_tocos_playoffs.BLK[2]) + ' tocos' + '\n' + str(df_tocos_playoffs.PLAYER[3]) + ' - ' + str(df_tocos_playoffs.BLK[3]) + ' tocos' + '\n' + str(df_tocos_playoffs.PLAYER[4]) + ' - ' + str(df_tocos_playoffs.BLK[4]) + ' tocos'


####################################### TEMPORADA REGULAR !!! ########################################################

    # Lideres totais em pontos na temporada
    data_pontos = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season)
    df_pontos = data_pontos.league_leaders.get_data_frame()
    pontos_totais = 'NBA - Top 5 da temporada: Pontos totais ' + '\n' + '\n' + str(df_pontos.PLAYER[0]) + ' - ' + str(df_pontos.PTS[0]) + ' pontos' + '\n' + str(df_pontos.PLAYER[1]) + ' - ' + str(df_pontos.PTS[1]) + ' pontos' + '\n' + str(
        df_pontos.PLAYER[2]) + ' - ' + str(df_pontos.PTS[2]) + ' pontos' + '\n' + str(df_pontos.PLAYER[3]) + ' - ' + str(df_pontos.PTS[3]) + ' pontos' + '\n' + str(df_pontos.PLAYER[4]) + ' - ' + str(df_pontos.PTS[4]) + ' pontos'

    # Lideres em rebotes totais na temporada
    data_rebotes = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, stat_category_abbreviation='REB')
    df_rebotes = data_rebotes.league_leaders.get_data_frame()
    rebotes_totais = 'NBA - Top 5 da temporada: Rebotes totais' + '\n' + '\n' + str(df_rebotes.PLAYER[0]) + ' - ' + str(df_rebotes.REB[0]) + ' rebotes' + '\n' + str(df_rebotes.PLAYER[1]) + ' - ' + str(df_rebotes.REB[1]) + ' rebotes' + '\n' + str(
        df_rebotes.PLAYER[2]) + ' - ' + str(df_rebotes.REB[2]) + ' rebotes' + '\n' + str(df_rebotes.PLAYER[3]) + ' - ' + str(df_rebotes.REB[3]) + ' rebotes' + '\n' + str(df_rebotes.PLAYER[4]) + ' - ' + str(df_rebotes.REB[4]) + ' rebotes'

    # Lideres em assistencias totais da temporada
    data_assistencias = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, stat_category_abbreviation='AST')
    df_assistencias = data_assistencias.league_leaders.get_data_frame()
    assistencias_totais = 'NBA - Top 5 da temporada: Assistencias totais' + '\n' + '\n' + str(df_assistencias.PLAYER[0]) + ' - ' + str(df_assistencias.AST[0]) + ' assistencias' + '\n' + str(df_assistencias.PLAYER[1]) + ' - ' + str(df_assistencias.AST[1]) + ' assistencias' + '\n' + str(
        df_assistencias.PLAYER[2]) + ' - ' + str(df_assistencias.AST[2]) + ' assistencias' + '\n' + str(df_assistencias.PLAYER[3]) + ' - ' + str(df_assistencias.AST[3]) + ' assistencias' + '\n' + str(df_assistencias.PLAYER[4]) + ' - ' + str(df_assistencias.AST[4]) + ' assistencias'

    # Lideres em roubos de bola totais na temporada
    data_roubos = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, stat_category_abbreviation='STL')
    df_roubos = data_roubos.league_leaders.get_data_frame()
    roubos_totais = 'NBA - Top 5 da temporada: Roubos de bola totais' + '\n' + '\n' + str(df_roubos.PLAYER[0]) + ' - ' + str(df_roubos.STL[0]) + ' roubos' + '\n' + str(df_roubos.PLAYER[1]) + ' - ' + str(df_roubos.STL[1]) + ' roubos' + '\n' + str(
        df_roubos.PLAYER[2]) + ' - ' + str(df_roubos.STL[2]) + ' roubos' + '\n' + str(df_roubos.PLAYER[3]) + ' - ' + str(df_roubos.STL[3]) + ' roubos' + '\n' + str(df_roubos.PLAYER[4]) + ' - ' + str(df_roubos.STL[4]) + ' roubos'

    # Lideres em tocos totais na temporada
    data_tocos = endpoints.leagueleaders.LeagueLeaders(
        season=SeasonAll.current_season, stat_category_abbreviation='BLK')
    df_tocos = data_tocos.league_leaders.get_data_frame()
    tocos_totais = 'NBA - Top 5 da temporada: Tocos totais' + '\n' + '\n' + str(df_tocos.PLAYER[0]) + ' - ' + str(df_tocos.BLK[0]) + ' tocos' + '\n' + str(df_tocos.PLAYER[1]) + ' - ' + str(df_tocos.BLK[1]) + ' tocos' + '\n' + str(
        df_tocos.PLAYER[2]) + ' - ' + str(df_tocos.BLK[2]) + ' tocos' + '\n' + str(df_tocos.PLAYER[3]) + ' - ' + str(df_tocos.BLK[3]) + ' tocos' + '\n' + str(df_tocos.PLAYER[4]) + ' - ' + str(df_tocos.BLK[4]) + ' tocos'

    dia = date.weekday(date.today())

    if dia == 0:
        logger.info('Segunda-feira ! Postando lideres em pontos nos playoffs.')
        api.update_status(pontos_totais_playoffs)
        logger.info("Esperando timer: 24 horas...")
        time.sleep(86400)
        return

    if dia == 1:
        logger.info('Terça-feira ! Postando lideres em rebotes nos playoffs.')
        api.update_status(rebotes_totais_playoffs)
        logger.info("Esperando timer: 24 horas...")
        time.sleep(86400)
        return

    if dia == 2:
        logger.info(
            'Quarta-feira ! Postando lideres em assistências nos playoffs.')
        api.update_status(assistencias_totais_playoffs)
        logger.info("Esperando timer: 24 horas...")
        time.sleep(86400)
        return

    if dia == 3:
        logger.info('Quinta-feira ! Postando lideres em roubos nos playoffs.')
        api.update_status(roubos_totais_playoffs)
        logger.info("Esperando timer: 24 horas...")
        time.sleep(86400)
        return

    if dia == 4:
        logger.info('Sexta-feira ! Postando lideres em tocos nos playoffs.')
        api.update_status(tocos_totais_playoffs)
        logger.info("Esperando timer: 24 horas...")
        time.sleep(86400)
        return

    if dia == 5:
        logger.info('Sábado ! Postando coisas aleatórias')
        api.update_status('boa noite randoms.')
        logger.info("Esperando timer: 24 horas...")
        time.sleep(86400)
        return

    if dia == 6:
        logger.info('Domingo ! Postando coisas aleatórias.')
        api.update_status('^~^')
        logger.info("Esperando timer: 24 horas...")
        time.sleep(86400)
        return

    # if last_tweeted < datetime.now()-timedelta(hours=12):
    #     api.update_status(pontos_totais)
    #     logger.info('Stats publicado com sucesso !')
    #     return datetime.now()
    # else:
    #     logger.info('Não é hora de publicar...')
    #     return last_tweeted


def main(api):

    while True:
        # like(api)
        follow_followers(api)
        daily_tweet(api)


if __name__ == "__main__":
    main(create_api())
