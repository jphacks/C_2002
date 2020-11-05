# coding: UTF-8

from flask import Flask, request
import os
import configparser
from goolabs import GoolabsAPI
import json
import requests
import re
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからgooラボAPIに関する情報を取得
Goo_API_APPLICATION_ID = config.get("Goo_API", "ApplicationId")
# 設定ファイルからRECRUITのAPIに関する情報を取得
RECRUITE_API_PROOFREADING_API_KEY = config.get("RECRUITE_API", "ProofreadingAPIKey")
RECRUITE_API_PROOFREADING_URL = config.get("RECRUITE_API", "ProofreadingURL")

# JSON送信用のヘッダー
headers= {
    "Content-type": "application/json"
}

# gooラボAPIのAPIクライアント設定
gooAPI = GoolabsAPI(Goo_API_APPLICATION_ID)

## 辞書データ取得
json_open = open(APP_ROOT + '/dict.json', 'r')
HumbleLangDict = json.load(json_open)

## 名詞用辞書データ取得
json_open = open(APP_ROOT + '/noun.json', 'r')
HumbleNounDict = json.load(json_open)

# 探索の省略が可能な品詞（Part of speech to omit）
Posto = ['句点', '読点', '空白', '格助詞', '終助詞', '括弧', '助数詞', '助助数詞', '冠数詞']

# 人名と会社名をリストで取得する関数
def get_list_people_companies(sentence):
    # print('get_list_people_companies Start')
    response = gooAPI.entity(sentence=sentence)
    people_name = list(set([people[0] for people in response['ne_list'] if people[1]=='PSN']))
    # print(people_name)
    companies_name = list(set([company[0] for company in response['ne_list'] if company[1]=='ORG']))
    # print(companies_name)
    return people_name, companies_name

# 校正支援をリストで取得する関数
def get_list_roofreading(text):
    # print('get_list_roofreading Start')
    # sentences = re.split('[、。，．,.!！？?"「」]', text)
    # morph = gooAPI.morph(sentence = text)
    response_list = []
    result_list = []
    sentence = text
    
    # Proofreading APIへのGET通信
    response_proofreading = requests.get(RECRUITE_API_PROOFREADING_URL + '?apikey=' + RECRUITE_API_PROOFREADING_API_KEY + '&sentence=' + sentence[0])
    response_list.append(response_proofreading.json())
    for res in response_list:
        if res['message']!='ok':
            result = {
                'inputSentence': res['inputSentence'],
                'checkedSentence': res['checkedSentence'],
                'alerts': res['alerts']
            }
            result_list.append(result)
            print(res['alerts'])
    # print(result_list)
    return result_list

# 単語探索関数
def SearchForWords(sentence):
    for start in range(len(sentence)):
        for end in range(len(sentence) - 1, start - 1, -1):
            testKey = ''
            for check in range(start, end + 1):
                testKey += sentence[check][0]
            if testKey in HumbleLangDict:
                if testKey not in HitWordList:
                    HitWordList.append(testKey)

# 単語置き換え用関数
def ChangeWord(text, HitWordList):
    ConvertedText = text
    for word in HitWordList:
        ConvertedText = ConvertedText.replace(word, HumbleLangDict[word])
    return ConvertedText

# 敬語変換関数
def ChangeToHonorific(original):
    # See sample response below.
    response = gooAPI.morph(sentence = original)

    # 形態素解析のデータの抽出
    originalData = response['word_list'][0]
    # print(originalData)

    ## 変換が必要な箇所を探索する
    for start in range(len(originalData)):
        ## 名詞の敬語に変換
        # ひとつ前に冠名詞がないか確認
        if start > 0 and originalData[start - 1][1] != '冠名詞':
            # 品詞の確認
            if originalData[start][1] == '名詞':
                # 名詞用辞書に登録されているか確認
                if originalData[start][0] in HumbleNounDict:
                    # 辞書に登録されていれば敬語に変換
                    originalData[start][0] = HumbleNounDict[originalData[start][0]]

        ## 名詞以外を警護に変換
        # 探索する必要がある品詞か判定
        if originalData[start][1] not in Posto or re.search(r'(\W)', originalData[start][1]) == 'None':
            # 辞書にヒットする語句を探索
            for end in range(len(originalData) - 1, start - 1, -1):
                testKey = ''
                # 辞書の検索にかける文字列の生成
                for check in range(start, end + 1):
                    testKey += originalData[check][0]
                # 文字列が辞書に登録されているか確認
                if testKey in HumbleLangDict:
                    # 辞書に登録されていた敬語に文字列を変換する
                    for i in range(start, end):
                        originalData[i][0] = ""
                    originalData[end][0] = HumbleLangDict[testKey]

    # 形態素解析のデータを敬語に変換したものを返す
    ConvertedData = originalData

    # 形態素解析のデータを敬語に変換したものを文に整形
    ConvertedSentence = ""
    for word in ConvertedData:
        ConvertedSentence += word[0]
    # 整形したデータを返す
    return ConvertedSentence

# ローカルGETテスト用
@app.route('/')
def hello():
    name = "Hello World"
    return name

# ローカルPOSTテスト用
@app.route('/test', methods=['POST'])
def post_test():
    # Node.jsからのPOST
    json_file = request.get_json()
    print(json_file['people_name'])
    print(json_file['companies_name'])

    # PythonからのPOST
    # print(request.form['people_name'])
    # print(request.form['companies_name'])
    return 'Success'

@app.route('/getdata')
def get_data():
    # 例文のテキストファイル読み込み
    f = open(APP_ROOT + "/before.txt", "r", encoding="utf-8")
    sentence = f.read()
    commit_id = '1c40b98'

    # 文章が空だった場合
    if sentence == '':
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'people_name_list': [],
            'companies_name_list': [],
            'before_sentence_calibration': [],
            'change_sentence': ''
        }

    else :
        with ThreadPoolExecutor(max_workers=3, thread_name_prefix="thread") as executor:
            # 人名と会社名をリストで取得
            people_name_list, companies_name_list = executor.submit(get_list_people_companies, sentence).result()
            # 校正支援をリストで取得
            result_before_text_calibration_list = executor.submit(get_list_roofreading, sentence).result()
            # 敬語変換
            change_text = executor.submit(ChangeToHonorific, sentence).result()
            # 敬語変換後の校正支援をリストで取得
            # result_change_text_calibration_list = executor.submit(get_list_roofreading, change_text).result()

        # # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'people_name_list': people_name_list,
            'companies_name_list': companies_name_list,
            'before_sentence_calibration': result_before_text_calibration_list,
            'change_sentence': change_text
            # 'change_sentence_calibration': result_change_text_calibration_list
        }
    f.close()
    return result

@app.route('/postdata', methods=['POST'])
def post_data():
    json_post = request.get_json()
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'people_name_list': [],
            'companies_name_list': [],
            'before_sentence_calibration': [],
            'change_sentence': ''
        }

    else :
        with ThreadPoolExecutor(max_workers=3, thread_name_prefix="thread") as executor:
            # 人名と会社名をリストで取得
            people_name_list, companies_name_list = executor.submit(get_list_people_companies, sentence).result()
            # 校正支援をリストで取得
            result_before_text_calibration_list = executor.submit(get_list_roofreading, sentence).result()
            # 敬語変換
            change_text = executor.submit(ChangeToHonorific, sentence).result()
        
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'people_name_list': people_name_list,
            'companies_name_list': companies_name_list,
            'before_sentence_calibration': result_before_text_calibration_list,
            'change_sentence': change_text
        }
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)