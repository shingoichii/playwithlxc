# LXDで40人分のLinuxログイン環境を作ってみた

* starter.sh --- 主スクリプト。標準入力からユーザリストを読ませる
* mkuserlist.py --- ユーザリストを生成
* userlist.txt --- 生成されたユーザリストの例
* setup.sh --- starter.sh内部で使用。コンテナにpushしてユーザ設定を行う
* wait_container.py --- starter.sh内部で使用。コンテナが立ち上がるのを待つ
* wait_address.py --- starter.sh内部で使用。コンテナにIPアドレスが割り当てられるのを待つ
* purgeall.sh --- 生成されたコンテナを一気にstop & deleteする
* prephome.sh --- コンテナ用のホームディレクトリを作る
* addr.py --- 試行錯誤していた時にテスト用に作ったもの
* wh.sh --- 試行錯誤していた時にテスト用に作ったもの
* starter.py --- 試行錯誤していた時にテスト用に作ったもの。一応動く
* README.md --- このファイル

## 使い方
### サーバ上の準備
Ubuntu 18.04を仮定

### lxdインストール
```
$ sudo snap install lxd
$ sudo apt install btrfs-progs
```

### lxd初期化
```
$ sudo lxd init
(block deviceをbtrfsにする以外はdefault)
```

### コンテナのユーザリスト生成
```
$ ./mkuserlist.py > userlist.txt
```

### サーバ上のユーザ追加
```
$ sudo adduser --no-create-home --disabled-login --gecos "" ksuser
$ id ksuser
uid=1001(ksuser) gid=1001(ksuser) groups=1001(ksuser)
$ sudo vi /etc/subuid
（root:1001:1を追加）
$ sudo vi /etc/subgid
（同上）
```

このユーザをコンテナ内のrootにmapする。

### コンテナ内のホームになるディレクトリを用意
```
$ sudo mkdir /home/prj
$ sudo chwon ksuser.ksuser /home/prj
$ sudo ./prephome.sh
```

`/home/prj/00`から`/home/prj/39`が作られる
（user/groupはksuser）。
それぞれが各コンテナの`/home/ks`にmountされる。
その下にコンテナ内のユーザのホームディレクトリが作られる。

### コンテナの生成と起動
```
$ ./starter.sh < userlist.txt
```

### 確認
```
$ lxc list
$ lxc exec exp00 bash
```

### 他のホストからの確認
```
$ ssh [サーバのIPアドレス] -p 20022 -l ksuser00
（ユーザ名、ポート番号、初期パスワードはuserlist.txtにあり）
```
