# airshift_print
 
airshiftの当日プリントを行うツールです。
また、白黒化も行います。

# 準備

- python
- pip
- pip install Pillow
- pip install selenium
- pip install pyyaml


以下ファイル、フォルダの作成
- config/config.yml
  - 中身
    - ID   : airシフトのID
    - PASS : airシフトのPASS
    - FILE : 例：「../result/result.png」
    - SITE : 拠点が複数ある場合を想定している。上から何番目か(0始まり)
- result

