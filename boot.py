import time
import utime
import network
import webrepl
import get_sensor_info
import send


#　WIFI設定を記述
SSID_NAME = "*****"
SSID_PASS = "*****"
REPL_PASS = "1234"


def connect_wifi(ssid, passkey, timeout=10):
    wifi= network.WLAN(network.STA_IF)
    if wifi.isconnected():
        print('already Connected. connect skip')
        return wifi
    else :
        wifi.active(True)
        count = 0
        while count < 5:
            try:
                wifi.connect(ssid, passkey)
                break
            except:
                utime.sleep(3)
                count += 1
        while not wifi.isconnected() and timeout > 0:
            print('.')
            utime.sleep(1)
            timeout -= 1
    if wifi.isconnected():
        print('Connected')
        webrepl.start(password=REPL_PASS)
        return wifi
    else:
        print('Connection failed!')
        return ''
    
   
def main():
    wifi= network.WLAN(network.STA_IF)
    if wifi.isconnected():
        connect_wifi(SSID_NAME, SSID_PASS)
    else:
        connect_wifi(SSID_NAME, SSID_PASS)
        send.send_start_time()
        file_info = get_sensor_info.main()


if __name__ == '__main__':
    main()
