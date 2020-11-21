import os
import configparser
from goolabs import GoolabsAPI
import json

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからgooラボAPIに関する情報を取得
Goo_API_APPLICATION_ID = config.get("Goo_API", "ApplicationId")

# gooラボAPIのAPIクライアント設定
gooAPI = GoolabsAPI(Goo_API_APPLICATION_ID)


def get_time(original):
    # See sample response below.
    response = gooAPI.entity(sentence=sentence)

    print(response)

    date_list = list([time[0] for time in response['ne_list'] if time[1]=='DAT'])
    time_list = list([time[0] for time in response['ne_list'] if time[1]=='TIM'])
    
    date = gooAPI.chrono(sentence=date_list[0])
    
    print(date)
    date_str = date['datetime_list'][0][1].split('-')
    # print(date)
    minutes_start_str = time_list[0].split(':')
    minutes_start = int(minutes_start_str[0])*60 + int(minutes_start_str[1])
    minutes_end_str = time_list[1].split(':')
    minutes_end = int(minutes_end_str[0])*60 + int(minutes_end_str[1])
    # print(minutes_end - minutes_start)
    datetime_list = [[int(date_str[0]), int(date_str[1]), int(date_str[2]), int(minutes_start_str[0]), int(minutes_start_str[1])], minutes_end - minutes_start]
    print(datetime_list)

sentence = '・11月1日（日）10:00～11:30'

get_time(sentence)
