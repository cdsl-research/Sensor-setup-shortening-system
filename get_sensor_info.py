from machine import Pin, I2C
import time
import urequests
import ujson
import utime
import os


def main():
    # I2Cバスを初期化 (I2Cのピンはデバイスにより異なります)
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)  # sclとsdaピンは例
    # スキャンを実行
    I2C_devices = i2c.scan()
    I2C_device = hex(0)
    
    sensor_info = dict()
    file_info = dict()

    if(I2C_devices):
        for I2C_device in I2C_devices:
            print(hex(I2C_device))
    else:
        print("I2Cに接続しているセンサーが見つかりませんでした")
    
    # 実行
    sensor_info = scan_register(I2C_device, i2c)
    file_info = send_info(sensor_info)
    
    #for i in file_info["files"]:
    #    get_file(file_info["name"], i)
        
    return file_info

def scan_register(I2C_addr, i2c):
    
    r_reg_count = 0
    values = []
    sensor_info = dict()
    
    print("IDレジスタを探索中...")
    for reg in range(0x00, 0xFF+1):
        try:
            # 各レジスタアドレスから1バイト読み取る
            data = i2c.readfrom_mem(I2C_addr, reg, 1)
            values.append(data[0])
            
            r_reg_count += 1
            if(reg == 0xD0):
                print(f"0xD0: {hex(values[reg])}")
            time.sleep(0.01)  # 少しウェイトを入れてI2Cを安定させる
        except Exception as e:
            # 読み取りに失敗した場合は無視
            values.append(-1)
    
    values.append(-1)
    
    print(f"I2Cアドレス{I2C_addr}, レジスタの値{values}, 読み取り可能レジスタ数{r_reg_count}")
    sensor_info = {"I2C_addr": I2C_addr, "register_num": values, "readable_register_num": r_reg_count}
    return sensor_info
    
        
def send_info(sensor_info):
    
    SERVER_URL = "http://192.168.100.197:8000/api/sensor-info"
    result = dict()
    
    try:
        
        headers = {"Content-Type": "application/json"}
        # POSTリクエスト送信
        response = urequests.post(SERVER_URL, headers=headers, data=ujson.dumps(sensor_info))
        # レスポンス確認
        if response.status_code == 200:
            result = ujson.loads(response.text)
            print(result["name"]) 
        else:
            print("Failed to download the file. Status code:", response.status_code)

        response.close()
        return result
    
    except Exception as e:
        print("Failed to send data:", e)


def get_file(dirname, filename):
    
    SERVER_URL = "http://192.168.100.197:8000/scripts"
    SAVE_DIR = f"/{dirname}"
    SAVE_FILE = f"{SAVE_DIR}/{filename}"
    
    try:
        os.mkdir(SAVE_DIR)
        print(f"{SAVE_DIR} created")
    
    except OSError as e:
        print(f"{SAVE_DIR} is already exists or error: {e}")
    
    try:
        headers = {"Content-Type": "application/json"}
        # POSTリクエスト送信
        response = urequests.get(f"{SERVER_URL}/{dirname}/{filename}")
        # レスポンス確認
        if response.status_code == 200:
            with open(SAVE_FILE, "wb") as f:
                f.write(response.content)
                print(f"File {filename} downloaded and saved as {SAVE_FILE}")
                
        else:
            print(f"Failed to download {filename}: {response.status_code}")
            
        response.close()
    except Exception as e:
        print(f"Error downloading file {filename}: {e}")
    
     
if __name__ == "__main__":
    main()
