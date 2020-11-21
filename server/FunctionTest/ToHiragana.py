import os
import configparser
from goolabs import GoolabsAPI
import json
import operator

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからgooラボAPIに関する情報を取得
Goo_API_APPLICATION_ID = config.get("Goo_API", "ApplicationId")

# gooラボAPIのAPIクライアント設定
gooAPI = GoolabsAPI(Goo_API_APPLICATION_ID)

# 名前を50音順にソートする関数
def sort_name(list):
    name_list = []
    for name in list:
       response = gooAPI.hiragana(sentence=name, output_type="hiragana")
       response['before'] = name
    #    print(response)
       name_list.append(response)
    name_sort_list = sorted(name_list, key=operator.itemgetter('converted'))
    return name_sort_list

arr = [ '高尾', '大羽', '岡崎', '近藤', '石倉' ];
print(sort_name(arr))