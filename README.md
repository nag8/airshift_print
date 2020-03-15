# airshift_print
 
airshiftの当日プリントを行うツールです。
また、白黒化も行います。

# 準備
## pythonのインストール
https://prog-8.com/docs/python-env

## pipのインストール
https://4to.pics/article/post/54

## slack_catの設定
https://qiita.com/keitatata/items/91e0f333061f88285b22

## 他コマンド
- pip install Pillow
- pip install selenium
- pip install pyyaml

## 他設定
以下ファイル、フォルダの作成
- config/config.yml
  - 中身
    - ID   : airシフトのID
    - PASS : airシフトのPASS
    - FILE : 例：「../result/result.png」
    - SITE : 拠点が複数ある場合を想定している。上から何番目か(0始まり)
- result

送信に利用するGmailアカウントで「安全性の低いアプリのアクセス」を許可する必要がある。
Googleアカウント「セキュリティ」の下部にて設定する。
(https://myaccount.google.com/security)


