import network
import urequests
import ujson
import time


SERVER_URL = "http://192.168.100.197:8000/api"

def send_data(data):
    result = str()
    
    try:
        headers = {"Content-Type": "application/json"}
        # POSTリクエスト送信
        response = urequests.post(f"{SERVER_URL}/send-data", headers=headers, data=ujson.dumps(data))
        # レスポンス確認
        if response.status_code == 200:
            result = response.text
            print(result) 
        else:
            print("Failed to download the file. Status code:", response.status_code)

        response.close()
    
    except Exception as e:
        print("Failed to send data:", e)


def send_start_time():
    result = str()
    data = {"message": "start"}
    try:
        headers = {"Content-Type": "application/json"}
        # POSTリクエスト送信
        response = urequests.post(f"{SERVER_URL}/get-start-time", headers=headers, data=ujson.dumps(data))
        # レスポンス確認
        if response.status_code == 200:
            result = response.text
            print(result) 
        else:
            print("Failed to send start time Status code:", response.status_code)

        response.close()
    
    except Exception as e:
        print("Failed to send data:", e)
    
    
# メイン処理
def main(data):
        # 送信するデータを定義
        send_info = {"jikken": "ari_yamamoto", "data": data}
        print(send_info)
        send_data(send_info)
