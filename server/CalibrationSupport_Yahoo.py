# -*- coding:utf-8 -*-

import os
import configparser
import requests
import json
import xml.etree.ElementTree as ET

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからYahooAPIに関する情報を取得
YAHOO_API_CLIENT_ID = config.get("Yahoo_API", "ClientId")
YAHOO_API_CALIBRATION_SUPPORT_URL = config.get("Yahoo_API", "CalibrationSupportURL")

# JSON送信用のヘッダー
headers= {
    "Content-type": "application/json"
}

# 校正支援をJSON形式で取得する関数
def get_json_calibration_support(sentence):
    # YahooAPI校正支援へのGET通信
    response = requests.get(str(YAHOO_API_CALIBRATION_SUPPORT_URL) + '?appid=' + YAHOO_API_CLIENT_ID + '&sentence=' + sentence)
    # responseをXML形式へ変換
    response_xml = ET.fromstring(response.text)
    # XML形式をJSON形式へ変換
    list_result = []
    for results in response_xml:
        result={}
        for index in results:
            result[index.tag.split('}')[1]] = index.text
        list_result.append(result)
    return json.dumps(list_result, ensure_ascii=False)

# 校正支援テスト用の文
sentence = '遙か彼方に小形飛行機が見えた'

# 校正支援をJSON形式で取得
result_calibration_json = get_json_calibration_support(sentence)
result_calibration_json = {
    'calibration': result_calibration_json
}
res = requests.post('http://localhost:5000/test', result_calibration_json, headers)
print(res.text)