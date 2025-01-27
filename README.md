# Sensor Setup Shortening System (4S)

# 用途・目的

これらのファイルはセンサーの識別と，センサーに対応したプログラムファイルの送受信に関するプログラムである．
クライアントにはget_sensor_info.py，サーバーにはmain.pyを実装する．これらのプログラムについて説明する．
クライアントに取り付けてあるセンサーからI2Cアドレス，レジスタの値を取得し，それらをサーバーに送信する．サーバーは受信したデータを，あらかじめ作成しておいたデータベース(DB)で検索する．検索がヒットすれば対応するPythonファイルの一覧をクライアントに送信する．クライアントは受信したPythonファイルの一覧から，全てのPythonファイルをサーバーに要求し，サーバーは要求からPythonファイルをクライアントに返す．

# 使用したクライアントとサーバーのハードウェア
クライアントはESP32を使用した．クライアントにはget_sensor_info.pyとboot.pyがある．
サーバーには、ESXiをもちいて，仮想マシンを作成した．サーバーにはmain.pyがある．
また，サーバーのホームディレクトリにはscriptsディレクトリを設置する必要がある．

# プログラムの紹介
## get_sensor_info.py
センサーからI2Cアドレス，レジスタの値のリスト，読み取り可能レジスタ数を取得し，サーバーに送信する．そして，サーバーから必要なPythonファイル一覧，センサー名を受け取り，センサー名のディレクトリを作成する．一覧の全てのPythonファイルをサーバーに要求し、受信したPythonファイルを保存する．

## main.py
クライアントからI2Cアドレス，レジスタの値のリスト，読み取り可能レジスタ数を受け取り，それらをDBで検索する．検索でヒットすれば，対応するPythonファイルの一覧とセンサー名を返す．

# 実行結果
## クライアント
BMP-280の場合

![image](https://github.com/user-attachments/assets/1ccb3f75-9da3-4903-8a86-f95907beb7ea)


BME-280の場合

![image](https://github.com/user-attachments/assets/b0dc871a-60ad-48a1-93bd-35fcfff19cfe)


ADT-7410の場合

![image](https://github.com/user-attachments/assets/9be709bc-962d-4f46-afbc-6f8c554148bd)


S-5851Aの場合

![image](https://github.com/user-attachments/assets/962e9bd4-014c-4cf9-b924-95720d6b9ff3)



## サーバー
BMP-280の場合

![image](https://github.com/user-attachments/assets/cec7a3ef-1c45-41b8-9cbd-4dfdad0861f0)


BME-280の場合

![image](https://github.com/user-attachments/assets/1850103b-bf48-4769-a591-8f393e2508ff)


ADT-7410の場合

![image](https://github.com/user-attachments/assets/1bd0e778-4868-4139-8d94-abaec72c4923)


S-5851Aの場合

![image](https://github.com/user-attachments/assets/b5c57549-de72-4c87-bf48-2e1657a994f1)

