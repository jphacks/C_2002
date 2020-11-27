import os
import datetime
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

# 時候の挨拶データ取得
json_open = open(APP_ROOT + '/seasonTemplate.json', 'r')
SeasonTemplate = json.load(json_open)

# 現在日時を取得
dt_now = datetime.datetime.now()
# print(SeasonTemplate[str(dt_now.month)])
# 結果をJSON形式にまとめる
result_season = {
    'greeting': SeasonTemplate[str(dt_now.month)]
}
print(result_season)
