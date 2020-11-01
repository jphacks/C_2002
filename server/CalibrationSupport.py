# -*- coding:utf-8 -*-

import os
import configparser
import requests
import xmljson
from lxml.etree import parse
import json
import xmltodict
import xml.etree.ElementTree as ET

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからYahooAPIに関する情報を取得
YAHOO_API_CLIENT_ID = config.get("Yahoo_API", "ClientId")
YAHOO_API_CALIBRATION_SUPPORT_URL = config.get("Yahoo_API", "CalibrationSupportURL")

headers= {
    "Content-type": "application/json"
}

# 校正支援テスト用の文
sentence = '遙か彼方に小形飛行機が見えた'

# YahooAPI校正支援へのGET通信
response_calibration = requests.get(str(YAHOO_API_CALIBRATION_SUPPORT_URL) + '?appid=' + YAHOO_API_CLIENT_ID + '&sentence=' + sentence)
# responseをXML形式へ変換
response_calibration_xml = ET.fromstring(response_calibration.text)
# XML形式をJSON形式へ変換
list_calibration = []
for results_calibration in response_calibration_xml:
    result_calibration={}
    for index_calibration in results_calibration:
        # print(index_calibration.tag, index_calibration.text)
        result_calibration[index_calibration.tag.split('}')[1]] = index_calibration.text
    list_calibration.append(result_calibration)
print(json.dumps(list_calibration))
result_calibration_json = {
    'calibration': json.dumps(list_calibration, ensure_ascii=False)
}
res = requests.post('http://localhost:5000/test', result_calibration_json, headers)
print(res)