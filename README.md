# airshift_print
 
airshiftの当日プリントを行うツールです。
また、白黒化も行います。

# 準備
## pythonのインストール
https://prog-8.com/docs/python-env

## pipのインストール
https://4to.pics/article/post/54

# chromeDriverのインストール
https://qiita.com/w5966qzh/items/4c1164bd7c611820c187#chrome%E3%81%AB%E5%90%88%E3%81%A3%E3%81%9F%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%81%AEwebdriver%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%97%E3%82%88%E3%81%86

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


