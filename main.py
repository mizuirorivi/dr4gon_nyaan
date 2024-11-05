import RPi.GPIO as GPIO
from RPLCD import CharLCD
import time
import netifaces
# 警告を無効化

def get_wlan0_ip():
    try:
        return netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    except (KeyError, ValueError):
        return "No IP address found for wlan0"
def split_string(text, chunk_size=32):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)

GPIO.setwarnings(False)

# GPIOモードをBCMに設定
GPIO.setmode(GPIO.BCM)

# LCDオブジェクトを初期化
lcd = CharLCD(cols=16, rows=2, pin_rs=18, pin_e=23, pins_data=[12,16,20,21],
              numbering_mode=GPIO.BCM)

ip = get_wlan0_ip()
chunks = split_string(ip)
for i in chunks:
    lcd.write.string(i)
    sleep(1)
