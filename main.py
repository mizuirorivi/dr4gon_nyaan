import RPi.GPIO as GPIO
from RPLCD import CharLCD
import time

# 警告を無効化
GPIO.setwarnings(False)

# GPIOモードをBCMに設定
GPIO.setmode(GPIO.BCM)

# LCDオブジェクトを初期化
lcd = CharLCD(cols=16, rows=2, pin_rs=18, pin_e=23, pins_data=[12, 16, 20, 21],
              numbering_mode=GPIO.BCM)

try:
    # LCDをクリア
    lcd.clear()
    
    # "Hello world!"を表示
    lcd.write_string("Hello world!")
    
    # 表示を確認するための待機時間
    time.sleep(5)

except KeyboardInterrupt:
    print("プログラムが中断されました")

except Exception as e:
    print(f"エラーが発生しました: {e}")

finally:
    # クリーンアップ
    lcd.close(clear=True)
    GPIO.cleanup()
    print("GPIOをクリーンアップしました")
