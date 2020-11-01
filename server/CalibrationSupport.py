# -*- coding:utf-8 -*-

import os
import configparser
import requests
import urllib.parse


# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからYahooAPIに関する情報を取得
YAHOO_API_CLIENT_ID = config.get("Yahoo_API", "ClientId")
YAHOO_API_CALIBRATION_SUPPORT_URL = config.get("Yahoo_API", "CalibrationSupportURL")

sentence = "私はその人の記憶を呼び起すごとに、すぐ「先生」といいたくなる".replace('、', '')

# sentence = '遙か彼方に小形飛行機が見える'

response = requests.get(str(YAHOO_API_CALIBRATION_SUPPORT_URL) + '?appid=' + YAHOO_API_CLIENT_ID + '&sentence=' + sentence)

# print(urllib.parse.quote(sentence))
print(response.text)