# airshift_print
 
airshiftの当日プリントを行うツールです。
また、白黒化も行います。

# 準備
## pythonのインストール
https://prog-8.com/docs/python-env

## poetryのインストール
https://kitigai.hatenablog.com/entry/2019/10/10/003422

## コマンド群
プロジェクト直下のディレクトリで実行してください。
```
$ mkdir result && mkdir config && touch config/config.yml
$ echo ID : <airシフトのID> >> config/config.yml
$ echo PASS : <airシフトのパスワード> >> config/config.yml
$ echo FILE : result/result.png >> config/config.yml
$ echo SLACK_CHANNEL : <投稿したいslackチャンネル名> >> config/config.yml
```

$ slackcat --configure

あとは以下サイトを参照
https://qiita.com/keitatata/items/91e0f333061f88285b22#%E8%A8%AD%E5%AE%9A


# 実行
```
$ poetry run python src/shift.py
$ poetry run python src/shift.py 20200530
```



# log
## 運用停止

送信に利用するGmailアカウントで「安全性の低いアプリのアクセス」を許可する必要がある。
Googleアカウント「セキュリティ」の下部にて設定する。
(https://myaccount.google.com/security)
