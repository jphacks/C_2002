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
import operator
import datetime
import CaboCha


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
json_open.close()

## 名詞用辞書データ取得
json_open = open(APP_ROOT + '/noun.json', 'r')
HumbleNounDict = json.load(json_open)
json_open.close()

#------------------------
json_open = open(APP_ROOT + '/AttributeDict.json', 'r', encoding='UTF-8')
AttributeDict = json.load(json_open)
json_open.close()

json_open = open(APP_ROOT + '/kana.json', 'r', encoding='UTF-8')
kana = json.load(json_open)
json_open.close()

json_open = open(APP_ROOT + '/InflectedForm.json', 'r', encoding='UTF-8')
InflectedForm = json.load(json_open)
json_open.close()

json_open = open(APP_ROOT + '/HumbleLanguage.json', 'r', encoding='UTF-8')
HumbleLanguage = json.load(json_open)
json_open.close()

json_open = open(APP_ROOT + '/RespectedWords.json', 'r', encoding='UTF-8')
RespectedWords = json.load(json_open)
json_open.close()

# 時候の挨拶データ取得
json_open = open(APP_ROOT + '/seasonTemplate.json', 'r')
SeasonTemplate = json.load(json_open)
json_open.close()

# 探索の省略が可能な品詞（Part of speech to omit）
Posto = ['句点', '読点', '空白', '格助詞', '終助詞', '括弧', '助数詞', '助助数詞', '冠数詞']

# 名前を50音順にソートする関数
def sort_name(list):
    name_list = []
    result_list = []
    for name in list:
       response = gooAPI.hiragana(sentence=name, output_type="hiragana")
       response['before'] = name
    #    print(response)
       name_list.append(response)
    name_sort_list = sorted(name_list, key=operator.itemgetter('converted'))
    for result in name_sort_list:
        result_list.append(result['before'])
    return result_list

# 人名と会社名,日時情報をリストで返す関数
def get_list_people_companies_time(sentence):
    # print('get_list_people_companies Start')
    response = gooAPI.entity(sentence=sentence)
    people_name = list(set([people[0] for people in response['ne_list'] if people[1]=='PSN']))
    # print(people_name)
    companies_name = list(set([company[0] for company in response['ne_list'] if company[1]=='ORG']))
    # print(companies_name)
    date_list = list([time[0] for time in response['ne_list'] if time[1]=='DAT'])
    time_list = list([time[0] for time in response['ne_list'] if time[1]=='TIM'])
    # print(date_list)
    # print(time_list)
    datetime_list = []
    if date_list and len(time_list)==2:
        date = gooAPI.chrono(sentence=date_list[0])
        date_str = date['datetime_list'][0][1].split('-')
        minutes_start_str = time_list[0].split(':')
        minutes_start = int(minutes_start_str[0])*60 + int(minutes_start_str[1])
        minutes_end_str = time_list[1].split(':')
        minutes_end = int(minutes_end_str[0])*60 + int(minutes_end_str[1])
        datetime_list = [[int(date_str[0]), int(date_str[1]), int(date_str[2]), int(minutes_start_str[0]), int(minutes_start_str[1])], minutes_end - minutes_start]
    return sort_name(people_name), sort_name(companies_name), datetime_list

# 人名をリストで返す関数
def get_list_people(sentence):
    text = sentence.split('\n')
    print(text)
    names = []
    for char in text:
        print(char)
        if char == "":
            continue
        response = gooAPI.entity(sentence=char)
        for people in response['ne_list']:
            if people[1]=='PSN':
                if people[0] not in names:
                    names.append(people[0])
    people_name = list(names)
    # print(people_name)
    return sort_name(people_name)

# 会社名をリストで返す関数
def get_list_companies(sentence):
    text = sentence.split('\n')
    names = []
    for char in text:
        if char == "":
            continue
        response = gooAPI.entity(sentence=char)
        for company in response['ne_list']:
            if company[1]=='ORG':
                if company[0] not in names:
                    names.append(company[0])
    companies_name = list(names)
    # print(companies_name)
    return sort_name(companies_name)

# 時刻情報をリストで返す関数
def get_list_time(sentence):
    response = gooAPI.entity(sentence=sentence)
    date_list = list([time[0] for time in response['ne_list'] if time[1]=='DAT'])
    time_list = list([time[0] for time in response['ne_list'] if time[1]=='TIM'])
    # print(date_list)
    # print(time_list)
    datetime_list = []
    if date_list and len(time_list)==2:
        date = gooAPI.chrono(sentence=date_list[0])
        date_str = date['datetime_list'][0][1].split('-')
        minutes_start_str = time_list[0].split(':')
        minutes_start = int(minutes_start_str[0])*60 + int(minutes_start_str[1])
        minutes_end_str = time_list[1].split(':')
        minutes_end = int(minutes_end_str[0])*60 + int(minutes_end_str[1])
        datetime_list = [[int(date_str[0]), int(date_str[1]), int(date_str[2]), int(minutes_start_str[0]), int(minutes_start_str[1])], minutes_end - minutes_start]
    return datetime_list

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

# # 単語探索関数
# def SearchForWords(sentence):
#     for start in range(len(sentence)):
#         for end in range(len(sentence) - 1, start - 1, -1):
#             testKey = ''
#             for check in range(start, end + 1):
#                 testKey += sentence[check][0]
#             if testKey in HumbleLangDict:
#                 if testKey not in HitWordList:
#                     HitWordList.append(testKey)

# # 単語置き換え用関数
# def ChangeWord(text, HitWordList):
#     ConvertedText = text
#     for word in HitWordList:
#         ConvertedText = ConvertedText.replace(word, HumbleLangDict[word])
#     return ConvertedText

# ## 活用形判断関数
def SV(source):
    # print("SV in")
    c = CaboCha.Parser()
    Q = source
    tree =  c.parse(Q)

    chunkId = 0
    sentence = []
    chunk = []
    S = []
    link = 0
    for i in range(0, tree.size()):
        token = tree.token(i)
        surface = token.surface
        feature = token.feature.split(",")
        if token.chunk != None:
            link = token.chunk.link
            # print(chunkId, link)
            if i != 0:
                sentence.append(chunk)
                chunk = []
            chunk.append(link)
            chunkId += 1
        chunk.append([surface, feature])

        # print(surface, feature)

        AttributeFlag = False

        if feature[0] == "名詞" and feature[1] == "一般":
            # print("AttributeFlag")
            AttributeFlag = True

        if feature[1] == "代名詞" or feature[2] == "人名" or AttributeFlag:
            # print(tree.token(i + 1).surface)
            if tree.size() > (i + 1):
                if tree.token(i + 1).surface == "は" or tree.token(i + 1).surface == "が":
                    # print("in")
                    if feature[6] in AttributeDict["I"]:
                        # print("I")
                        S.append([chunkId - 1, link, 1])
                    elif feature[6] in AttributeDict["You"] or feature[2] == "人名":
                        # print("You")
                        S.append([chunkId - 1, link, 2])
                    else:
                        S.append([chunkId - 1, link, 0])
        # print(chunk)
  
    sentence.append(chunk)
    return S, sentence

def MakeWord(V):
    word = ""
    for i in range(len(V)):
        word += V[i][0]
        if V[i][1][1] == "自立":
            return word
            
def ChangeToHonorificForVerb(original):
    # print(original)
    H_verb = []
    HL_verb = []
    S, sentence = SV(original)
    # print(S)
    if len(S) > 0:
        for i in range(len(S)):
            V = sentence[S[i][1]]
            V.pop(0)
            # print(V)
            if S[i][2] == 1:
                H_verb.append(MakeWord(V))
            elif S[i][2] == 2:
                HL_verb.append(MakeWord(V))
    return H_verb, HL_verb


def TransformVerb(V, Utilization):
    print(V[1])
    Verb = V[0]
    if V[1] == "五段":
        buff = Verb.pop(0)
        Verb += kana[buff][InflectedForm["五段"][Utilization]]
    elif V[1] == "一段":
        buff = Verb.pop(0)
        Verb += InflectedForm["一段"][Utilization]
    elif V[1] == "カ変":
        Verb = InflectedForm["カ変"][Utilization]
    elif V[1] == "サ変":
        Verb = Verb.replace("する", InflectedForm["サ変"][Utilization])
    return Verb

def ForVerb(original):
    H_verb, HL_verb = ChangeToHonorificForVerb(original)

    if len(H_verb) > 0:
        for i in range(len(H_verb)):
            if H_verb[i][1] in HumbleLanguage:
                V = TransformVerb(HumbleLanguage[H_verb[i][1]], H_verb[i][3])
                print(V)
                original = original.replace(H_verb[i][0], V)

    if len(HL_verb) > 0:
        for i in range(len(HL_verb)):
            if HL_verb[i][1] in RespectedWords:
                V = TransformVerb(HumbleLanguage[HL_verb[i][1]], HL_verb[i][3])
                print(V)
                original = original.replace(HL_verb[i][0], V)
    return original


## 形態素解析のデータを敬語に変換する関数
def DataConverter(sentence):
    # 探索の省略が可能な品詞（Part of speech to omit）
    Posto = ['句点', '読点', '空白', '格助詞', '終助詞', '括弧', '助数詞', '助助数詞', '冠数詞']
    
    ## 変換が必要な箇所を探索する
    for start in range(len(sentence)):
        ## 名詞の敬語に変換
        # ひとつ前に冠名詞がないか確認
        if start > 0 and sentence[start - 1][1] != '冠名詞':
            # 品詞の確認
            if sentence[start][1] == '名詞':
                # 名詞用辞書に登録されているか確認
                if sentence[start][0] in HumbleNounDict:
                    # 辞書に登録されていれば敬語に変換
                    sentence[start][0] = HumbleNounDict[sentence[start][0]]

        ## 名詞以外を敬語に変換
        # 探索する必要がある品詞か判定
        if sentence[start][1] not in Posto or re.search(r'(\W)', sentence[start][1]) == 'None':
            # 辞書にヒットする語句を探索
            for end in range(len(sentence) - 1, start - 1, -1):
                testKey = ''
                # 辞書の検索にかける文字列の生成
                for check in range(start, end + 1):
                    testKey += sentence[check][0]
                # 文字列が辞書に登録されているか確認
                if testKey in HumbleLangDict:
                    # 辞書に登録されていた敬語に文字列を変換する
                    for i in range(start, end):
                        sentence[i][0] = ""
                    sentence[end][0] = HumbleLangDict[testKey]

    # 形態素解析のデータを敬語に変換したものを返す
    return sentence


## 敬語変換関数
def ChangeToHonorific(original):
    original = ForVerb(original)

    # See sample response below.
    response = gooAPI.morph(sentence=original)

    # 形態素解析のデータの抽出
    originalData = response['word_list'][0]
    # print(originalData)

    # 形態素解析のデータを敬語に変換する関数の呼び出し
    ConvertedData = DataConverter(originalData)

    # 形態素解析のデータを敬語に変換したものを文に整形
    ConvertedSentence = ""
    for word in ConvertedData:
        ConvertedSentence += word[0]
    # 整形したデータを返す
    return ConvertedSentence

# # 敬語変換関数
# def ChangeToHonorific(original):
#     # See sample response below.
#     response = gooAPI.morph(sentence = original)

#     # 形態素解析のデータの抽出
#     originalData = response['word_list'][0]
#     # print(originalData)

#     ## 変換が必要な箇所を探索する
#     for start in range(len(originalData)):
#         ## 名詞の敬語に変換
#         # ひとつ前に冠名詞がないか確認
#         if start > 0 and originalData[start - 1][1] != '冠名詞':
#             # 品詞の確認
#             if originalData[start][1] == '名詞':
#                 # 名詞用辞書に登録されているか確認
#                 if originalData[start][0] in HumbleNounDict:
#                     # 辞書に登録されていれば敬語に変換
#                     originalData[start][0] = HumbleNounDict[originalData[start][0]]

#         ## 名詞以外を警護に変換
#         # 探索する必要がある品詞か判定
#         if originalData[start][1] not in Posto or re.search(r'(\W)', originalData[start][1]) == 'None':
#             # 辞書にヒットする語句を探索
#             for end in range(len(originalData) - 1, start - 1, -1):
#                 testKey = ''
#                 # 辞書の検索にかける文字列の生成
#                 for check in range(start, end + 1):
#                     testKey += originalData[check][0]
#                 # 文字列が辞書に登録されているか確認
#                 if testKey in HumbleLangDict:
#                     # 辞書に登録されていた敬語に文字列を変換する
#                     for i in range(start, end):
#                         originalData[i][0] = ""
#                     originalData[end][0] = HumbleLangDict[testKey]

#     # 形態素解析のデータを敬語に変換したものを返す
#     ConvertedData = originalData

#     # 形態素解析のデータを敬語に変換したものを文に整形
#     ConvertedSentence = ""
#     for word in ConvertedData:
#         ConvertedSentence += word[0]
#     # 整形したデータを返す
#     return ConvertedSentence


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
            'datetime_list': [],
            'before_sentence_calibration': [],
            'change_sentence': ''
        }

    else :
        with ThreadPoolExecutor(max_workers=3, thread_name_prefix="thread") as executor:
            # 人名と会社名をリストで取得
            people_name_list, companies_name_list, time_list = executor.submit(get_list_people_companies_time, sentence).result()
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
            'datetime_list': time_list,
            'before_sentence_calibration': result_before_text_calibration_list,
            'change_sentence': change_text
            # 'change_sentence_calibration': result_change_text_calibration_list
        }
    f.close()
    return result

@app.route('/getseason')
def get_season():
    # 現在日時を取得
    dt_now = datetime.datetime.now()
    
    # 結果をJSON形式にまとめる
    result_season = {
        'greeting': SeasonTemplate[str(dt_now.month)]
    }
    return result_season

@app.route('/postpeople', methods=['POST'])
def post_persons():
    json_post = request.get_json()
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'people_name_list': []
        }

    else :
        # 人名をリストで取得
        people_name_list = get_list_people(sentence)
        
        # 結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'people_name_list': people_name_list
        }
    return result

@app.route('/postcompanies', methods=['POST'])
def post_companies():
    json_post = request.get_json()
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'companies_name_list': []
        }

    else :
        # 会社名をリストで取得
        companies_name_list = get_list_companies(sentence)
        
        # 結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'companies_name_list': companies_name_list
        }
    return result

@app.route('/postnames', methods=['POST'])
def post_names():
    json_post = request.get_json()
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 全て結果をJSON形式にまとめて返す
        result = {
            'before_sentence': sentence,
            'people_name_list': [],
            'companies_name_list': []
        }

    else :
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as executor:
            # 人名をリストで取得
            people_name_list = executor.submit(get_list_people, sentence).result()
            # 会社名をリストで取得
            companies_name_list = executor.submit(get_list_companies, sentence).result()
        
        # 結果をJSON形式にまとめて返す
        result = {
            'before_sentence': sentence,
            'people_name_list': people_name_list,
            'companies_name_list': companies_name_list
        }
    return result

@app.route('/postdatetime', methods=['POST'])
def post_datetime():
    json_post = request.get_json()
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'datetime_list': []
        }

    else :
        # 日時情報をリストで取得
        time_list = get_list_time(sentence)
        
        # 結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'datetime_list': time_list
        }
    return result

@app.route('/postcalibration', methods=['POST'])
def post_calibration():
    json_post = request.get_json()
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'calibration_sentence': []
        }

    else :
        # 校正支援をリストで取得
        result_before_text_calibration_list = get_list_roofreading(sentence)
        
        # 結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'calibration_sentence': result_before_text_calibration_list
        }
    return result

@app.route('/postchange', methods=['POST'])
def post_change():
    json_post = request.get_json()
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'change_sentence': ''
        }

    else :
        # 敬語変換
        change_text = ChangeToHonorific(sentence)
        
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'change_sentence': change_text
        }
    return result

@app.route('/postchangecalibration', methods=['POST'])
def post_changecalibration():
    json_post = request.get_json()
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'change_sentence_calibration': [],
            'change_sentence': ''
        }

    else :
        # 敬語変換
        change_text = ChangeToHonorific(sentence)
        # 校正支援をリストで取得
        result_change_text_calibration_list = get_list_roofreading(change_text)
        
        # 全て結果をJSON形式にまとめて返す
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'change_sentence_calibration': result_change_text_calibration_list,
            'change_sentence': change_text
        }
    return result

@app.route('/postdata', methods=['POST'])
def post_data():
    json_post = request.get_json()
    commit_id = json_post['commit_id']
    sentence = json_post['sentence']

    # 文章が空だった場合
    if sentence == '':
        # 全ての結果をJSON形式にまとめて返す
        # result = {
        #     'commit_id': commit_id,
        #     'before_sentence': sentence,
        #     'people_name_list': [],
        #     'companies_name_list': [],
        #     'datetime_list': [],
        #     'before_sentence_calibration': [],
        #     'change_sentence': ''
        # }
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'people_name_list': [],
            'companies_name_list': [],
            'datetime_list': [],
            'change_sentence': ''
        }

    else :
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as executor:
            # 人名と会社名,日時情報をリストで取得
            people_name_list, companies_name_list, time_list = executor.submit(get_list_people_companies_time, sentence).result()
            # 校正支援をリストで取得
            # result_before_text_calibration_list = executor.submit(get_list_roofreading, sentence).result()
            # 敬語変換
            change_text = executor.submit(ChangeToHonorific, sentence).result()
        
        # 全ての結果をJSON形式にまとめて返す
        # result = {
        #     'commit_id': commit_id,
        #     'before_sentence': sentence,
        #     'people_name_list': people_name_list,
        #     'companies_name_list': companies_name_list,
        #     'datetime_list': time_list,
        #     'before_sentence_calibration': result_before_text_calibration_list,
        #     'change_sentence': change_text
        # }
        result = {
            'commit_id': commit_id,
            'before_sentence': sentence,
            'people_name_list': people_name_list,
            'companies_name_list': companies_name_list,
            'datetime_list': time_list,
            'change_sentence': change_text
        }
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)