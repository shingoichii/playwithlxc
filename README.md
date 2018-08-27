# LXDで40人分のLinuxログイン環境を作ってみた

* starter.sh --- 主スクリプト。標準入力からuserlist.txt相当の内容を読ませる
* mkuserlist.py --- userlist.txtを生成
* userlist.txt --- 生成されたユーザリストの例
* setup.sh --- starter.sh内部で使用。コンテナにpushしてユーザ設定を行う
* wait_container.py --- starter.sh内部で使用。コンテナが立ち上がるのを待つ
* wait_address.py --- starter.sh内部で使用。コンテナにIPアドレスが割り当てられるのを待つ
* purgeall.sh --- 生成されたコンテナを一気にstop & deleteする
* addr.py --- 試行錯誤していた時にテスト用に作ったもの
* wh.sh --- 試行錯誤していた時にテスト用に作ったもの
* starter.py --- 試行錯誤していた時にテスト用に作ったもの。一応動く
* README.md --- このファイル
