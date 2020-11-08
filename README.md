#  Frankfurt

ビジネスメールをフランクに書けるメールクライアント「Frankfurt」

[![IMAGE ALT TEXT HERE](https://github.com/jphacks/C_2002/wiki/images/pop-logo.png)](https://github.com/jphacks/C_2002/wiki/images/pop-logo.png)

## 紹介動画〜デモ入り〜

[![DEMO](https://github.com/jphacks/C_2002/blob/master/%E3%83%97%E3%83%AC%E3%82%BC%E3%83%B3/StartDemo.png?raw=true)](https://youtu.be/GHsLTyOwET8)

## アーキテクチャ

[![Architecture.png](https://github.com/jphacks/C_2002/blob/master/%E3%83%97%E3%83%AC%E3%82%BC%E3%83%B3/Architecture.png?raw=true)](https://github.com/jphacks/C_2002/blob/master/%E3%83%97%E3%83%AC%E3%82%BC%E3%83%B3/Architecture.png?raw=true)


## 製品概要

### ビジネスマナー × Tech

[![×TECH.png](https://github.com/jphacks/C_2002/blob/master/%E3%83%97%E3%83%AC%E3%82%BC%E3%83%B3/%C3%97TECH.png?raw=true)](https://github.com/jphacks/C_2002/blob/master/%E3%83%97%E3%83%AC%E3%82%BC%E3%83%B3/%C3%97TECH.png?raw=true)

### 背景(製品開発のきっかけ、課題等）
COVID-19(新型コロナウイルス)の影響により世の中で様々なことがオンライン化した中．
コミュニケーション様式も大きな影響を受け，**対人でのコミュニケーションからテキストベースに変化**している．
また，近年は，LINEといったチャット形式のコミュニケーションツールが普及し，若者がメール形式でコミュニケーションを行うことが減ったのもあり，
電子メールなどを作成する際に**適切な体裁や言葉遣いを意識しない**傾向にある．
こうした時代の変化から，私たちは「**テキストベースコミュニケーションが増加した中，メール形式に慣れていない若者が，適切な体裁・言葉遣いでビジネスメールを上手く作成できない**」ということを課題とした．

### 製品説明（具体的な製品の説明）
本製品は，**統合ビジネスメール作成環境(IBE)** の **デスクトップアプリ** である．

* 就職活動を行っている大学生と，若手社員のためのメールクライアントソフトウェア

* メール文をビジネスに即したメールに変換し，送信を行うことができる．

### 特長

#### 1. エンジニアが使うツールをユーザーのメール作成に落としこみ，意識することなく便利な機能を利用可能に

*  **Gitによるメール文の差分管理**

今回利用している「固有表現抽出API」や「形態素解析API」へのアクセスに時間がかかり、10行程度のメール文章で30秒程度変換にかかりました。
そこで高速化の方法として、Gitの機能である差分管理を導入し差分のみをAPIにPOSTすることで1文につき平均で2～3秒程度で変換結果が返ってくるようになりました。

![Gitによる校正箇所の割り出し](https://i.imgur.com/09zgMLA.png)

*  **メール校正の着想はエンジニアの校正ツールとも言えるIDEから**

私たちエンジニアが普段利用しているIDE（統合開発環境）に導入されているリフォーマット機能や訂正機能をメールに活かせないかと思いこのアイディアに至りました。
コードのデバッグやコンパイルのように、メールを作成した際に自動で校正や敬語変換を行い，丁寧な表現に変換ができます。
ON/OFFで切り替え可能なためカジュアルなメール送信も可能です。


#### 2. チャット形式のUI

- **現状のメールクライアントの課題**

SNSなどのチャットアプリケーションの利点の一つとして、ダイレクトメッセージ（通称：DM）による個別のチャットルームで会話の流れが分かり易いという点にあります。

▼実際のUI

![実際のUI](https://i.imgur.com/OTwjjhv.png)

現状のメールクライアントでは「受信トレイ」と「送信トレイ」とそれぞれ分かれています。

- 本当にメールを返信したのか？
- 相手から返信の来ていないメールがないか？

などの会話の流れが一目でわかり難いのも課題の1つです。
その不便さを改善するために、チャット式のUIを採用し会話の流れを可視化しました。

- **実装方法**

課題として、

- 送信したメールが格納される「SMTPサーバ」
- 受信したメールが格納される「IMAPサーバ」

から送受信メールを受け取り、時系列順に処理をすると処理が重くなると考えました。

▼現状のメールの流れ
![現状のメールの流れ](https://i.imgur.com/8nlEIIg.png)


そのため、今回は**送信するメール全てに対して、自分自身へのBCCを付ける**ことで「IMAPサーバ」に自信が送信したメールが送られるため、**「IMAP」サーバのみを参照するだけで送受信一覧を取得できる**という方法を考えました。

▼Frankfurtで送信するメールの流れ
![Franfurtでの流れ](https://i.imgur.com/PakpXQf.png)

これはあくまでFrankfurtから送信したメールに限っての話なので、課題でもあります。



### 解決出来ること

*   不適切なメール文での悪印象を回避．
    * ビジネスメールの不適切な表現を事前に修正する．

*  メールの見落としを回避
    *  メールの相手ごとにやりとりを分けた．
    *  送信・受信を色で分け，送受信の方向性が一目でわかる．

*  メールへの敬遠を防ぐ
    *  メール形式に慣れていない若者にも受け入れられやすいUIによって，若者のメール離れをつなぎ止め，ビジネスでのトラブルを減らす．

### 今後の展望

* ビジネスメールで頻繁に用いられる表現をサジェストして，文章補完を行えるようにする．
* メールクライアントに備わっている通常機能は設けたい
* スレッドをツリー形式で表示する

### 注力したこと（こだわり等）
* クロスプラットホームで，OSに関わらず使用することが可能
* 認証情報は，サーバーにあげずに保管するため，セキュリティ面も安心

## 開発技術

### 活用した技術

#### 使用言語

* HTML
* SCSS
* JavaScript
* Python 3

#### フレームワーク・ライブラリ・モジュール

* [Git](https://git-scm.com/)
* [Vue.js](https://jp.vuejs.org/index.html)
* [Node.js](https://nodejs.org/ja/)
* [Electron](https://www.electronjs.org/)
* [jQuery](https://jquery.com/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [MySQL](https://www.mysql.com/jp/)

#### API・データ

* スポンサー様の提供サービス
    * [goo ラボ API](https://labs.goo.ne.jp/)
        * [固有表現抽出API](https://labs.goo.ne.jp/api/jp/named-entity-extraction/)
        * [形態素解析API](https://labs.goo.ne.jp/api/jp/morphological-analysis/)
        * [時刻情報正規化API](https://labs.goo.ne.jp/api/jp/time-normalization)
* 外部サービス
    * [AWS EC2](https://aws.amazon.com/jp/ec2/?ec2-whats-new.sort-by=item.additionalFields.postDateTime&ec2-whats-new.sort-order=desc)
    * [Proofreading API](https://a3rt.recruit-tech.co.jp/product/proofreadingAPI/)

#### デバイス

* なし

#### その他

- 資料内画像：[Illustration by Freepik Stories](https://stories.freepik.com/work)

### 独自技術

#### ハッカソンで開発した独自機能・技術

* 独自で開発したものの内容をこちらに記載してください
* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください。
* アプリケーションの画面や画面遷移等
    * **[メールの送受信をチャット形式で表示](https://github.com/jphacks/C_2002/blob/master/front/src/renderer/components/columns/ChatTree.vue)**
    * [メールの作成画面](https://github.com/jphacks/C_2002/blob/master/front/src/renderer/components/columns/MailEditer.vue)
    * [校正画面](https://github.com/jphacks/C_2002/blob/master/front/src/renderer/components/columns/Preview.vue)
* アプリケーション本体の処理
    * [クライアント側の処理](https://github.com/jphacks/C_2002/tree/master/front/src)（Electron）
        * **[メール本文の差分管理](https://github.com/jphacks/C_2002/blob/master/front/src/renderer/utils/NodeGit.js)**（Git）
        * [クロスプラットフォーム対応](https://github.com/jphacks/C_2002/blob/master/front/src/renderer/utils/OS.js)
        * [メール送信](https://github.com/jphacks/C_2002/blob/master/front/src/renderer/utils/MailSend.js)
        * [メール受信](https://github.com/jphacks/C_2002/blob/master/front/src/renderer/utils/MailReceive.js)
    * [サーバ側の処理](https://github.com/jphacks/C_2002/blob/master/server/server.py)（AWS EC2）
        * **[敬語への変換](https://github.com/jphacks/C_2002/blob/master/server/FunctionTest/NewHonorificsConvert.py)**（形態素解析API，機械学習）
        * [人名と会社名の抽出](https://github.com/jphacks/C_2002/blob/master/server/FunctionTest/ExtractProperNoun.py)（固有表現抽出API）
        * [校正箇所の指摘](https://github.com/jphacks/C_2002/blob/master/server/FunctionTest/Proofreading_RECRUIT.py)（Proofreading API）
        * [日時情報の抽出](https://github.com/jphacks/C_2002/blob/master/server/FunctionTest/getTime.py)(時刻情報正規化API)

#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）
* なし

#### 事前開発プロダクト
* なし


## 開発チーム
### Pied Piper

* [RyogaTakao](https://github.com/RyogaTakao): サーバーサイド
* [YoshiharuSenna](https://github.com/YoshiharuSenna): サーバーサイド
* [ReERishun](https://github.com/ree-rishun): フロントエンド
* [OkazakiTatsuya](https://github.com/TatsuyaOkazaki324): フロントエンド
* [rappy-git](https://github.com/rappy-git): データサイエンティスト, 情報収集
* [Miyu Oba](https://github.com/mlieynua): データサイエンティスト, 情報収集
