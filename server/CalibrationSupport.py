# -*- coding:utf-8 -*-

import os
import configparser
import requests

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからYahooAPIに関する情報を取得
YAHOO_API_CLIENT_ID = config.get("Yahoo_API", "ClientId")


sentence = "私はその人の記憶を呼び起すごとに、すぐ「先生」といいたくなる"

data = {
    "appid":client_id,
    "results":"ma",
    "sentence":sentence
}

response = requests.post(target_url, data=data)

root = ET.fromstring(response.text)

for e in root.getiterator("{urn:yahoo:jp:jlp}surface"):
    print (e.text, end=" ")