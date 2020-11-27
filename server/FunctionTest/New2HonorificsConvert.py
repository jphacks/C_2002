import json
import CaboCha
import re
from goolabs import GoolabsAPI
import configparser
import os

# ソースファイルの場所取得
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# 設定ファイルの読み込み
config = configparser.ConfigParser()
config.read(APP_ROOT + '/config_local.ini')
# 設定ファイルからgooラボAPIに関する情報を取得
Goo_API_APPLICATION_ID = config.get("Goo_API", "ApplicationId")

# gooラボAPIのAPIクライアント設定
gooAPI = GoolabsAPI(Goo_API_APPLICATION_ID)

## 元のテキストデータ
f = open(APP_ROOT + '/before.txt', 'r', encoding='UTF-8')

## 辞書データ取得
json_open = open(APP_ROOT + '/dict.json', 'r', encoding='UTF-8')
HumbleLangDict = json.load(json_open)
json_open.close()

## 名詞用辞書データ取得
json_open = open(APP_ROOT + '/noun.json', 'r', encoding='UTF-8')
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

# テスト用に一行ずつ文を渡す
while True:
    original = f.readline()
    if original:
        ConvertedSentence = ChangeToHonorific(original)
        print('converted = ' + ConvertedSentence)   
    else:
        print('fin')
        break
f.close()