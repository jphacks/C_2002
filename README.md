# Frank Furt

[![IMAGE ALT TEXT HERE](https://github.com/jphacks/C_2002/wiki/images/pop-logo.png)](https://github.com/jphacks/C_2002/wiki/images/pop-logo.png)

## 製品概要

### ビジネスマナー × Tech

### 背景(製品開発のきっかけ、課題等）
COVID-19(コロナウイルス)の影響により世の中で様々なことがオンライン形態へと変化した．
その中でコミュニケーション形態もまた大きな影響を受けている．
コミュニケーション形態は，対面からビデオ会議やテキストベースに変化している．
こうした変化の中で起こりうる問題は様々であり，その中で私たちはテキストベースのコミュニケーションでの適切な言葉遣いという点に着目した．
近年では，チャット形式のコミュニケーションツールが普及し，電子メールなどを作成する際に適切な体裁や言葉遣いを意識しない傾向にある．
こうした傾向を背景にして私たちは「チャットに慣れた者が適切な体裁・言葉遣いが上手くできない」ということを課題とした．

### 製品説明（具体的な製品の説明）
本製品は，**統合的ビジネスメール作成環境(IBE)** の **デスクトップアプリ** である．

* 感覚的に利用することが可能
    * チャット感覚で利用可能なメールクライアントアプリケーション

* エンジニアが使う超有能ツールをユーザが意識することなく利用
    * gitによるバージョン管理
    * IDEのメリットを取り入れた
        * ソースコード補完 → フォーマルな文章補完
        * デバック → 文章校正
        * コンパイラ → 敬語変換
        * 統合環境上でビルド → アプリ上で送受信

### 特長

#### 1. メール本文を機械学習により自動校正
メール本文を作成した際に，目上の人に送信しても困らない文章に自動で校正する．

#### 2. よく使われる敬語表現を推測することにより文章補完
よく使われる定型文を推測し，最小の文字入力でサジェスト表示をして文章の補完を行う．

#### 3. クロスプラットフォームでアプリケーションを作成
クロスプラットフォームであるため，MacOSやWindows,Linuxなどの様々なOSでの利用が可能である．

### 解決出来ること
ビジネスメールのやりとりで生じる不適切なメール本文を事前に修正することで、メールでのコミュニケーションの悪印象を改善することができる．
メールのやりとりをメール相手によってフィルタリングし，さらに送受信の方向性を一目でわかるUIにしたことにより，メールの見落としをなくすことができる．

### 今後の展望
今後は対応できるメールサービスの数を増やし，一つのアプリケーションでの完結性を向上させる．

# **そのほかもあれば**

### 注力したこと（こだわり等）
* 機械学習により適切な文章へと校正できることはもちろん，その機能をONとOFFで切り替えることが可能
* 文章校正の高速化を行うために文章をGitにより差分管理し，差分のみを校正する機能を実装した
* チャット形態のコミュニケーションに慣れている人を対象にしていることから，そういった人が使いやすく馴染みやすいUIとしたこと
* メールクライアントアプリケーションとしてどんな人にでも使ってもらえるようなUIのシンプルさを考えて実装した

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

#### API・データ
* スポンサー様の提供サービス
    * [goo ラボ API](https://labs.goo.ne.jp/)
        * [固有表現抽出API](https://labs.goo.ne.jp/api/jp/named-entity-extraction/)
        * [形態素解析API](https://labs.goo.ne.jp/api/jp/morphological-analysis/)
* 外部サービス
    * [AWS EC2](https://aws.amazon.com/jp/ec2/?ec2-whats-new.sort-by=item.additionalFields.postDateTime&ec2-whats-new.sort-order=desc)
    * [Proofreading API](https://a3rt.recruit-tech.co.jp/product/proofreadingAPI/)

#### デバイス
* なし

### 独自技術
#### ハッカソンで開発した独自機能・技術
* 独自で開発したものの内容をこちらに記載してください
* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください。
* アプリケーションの画面や画面遷移等
* アプリケーション本体の処理
    * クライアント側の処理
    * サーバ側の処理（[AWS EC2](https://aws.amazon.com/jp/ec2/?ec2-whats-new.sort-by=item.additionalFields.postDateTime&ec2-whats-new.sort-order=desc)）
        * メール文から人名と会社名を抽出（[固有表現抽出API](https://labs.goo.ne.jp/api/jp/named-entity-extraction/)）
        * 校正箇所の指摘（[Proofreading API](https://a3rt.recruit-tech.co.jp/product/proofreadingAPI/)）
        * 敬語への変換（[形態素解析API](https://labs.goo.ne.jp/api/jp/morphological-analysis/)，機械学習）

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
