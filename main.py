import RPi.GPIO as GPIO
from RPLCD import CharLCD
import time
import netifaces

# 警告を無効化
GPIO.setwarnings(False)

# GPIOモードをBCMに設定
GPIO.setmode(GPIO.BCM)

# LCDオブジェクトを初期化
lcd = CharLCD(cols=16, rows=2, pin_rs=18, pin_e=23, pins_data=[12, 16, 20, 21],
              numbering_mode=GPIO.BCM)

def get_wlan0_ip():
    try:
        return netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    except (KeyError, ValueError):
        return "No IP address found for wlan0"

def scroll_text(text, lcd):
    # Fill the LCD with spaces initially
    lcd.clear()
    lcd.write_string(' ' * 16)  # Fill with spaces for smooth scrolling

    # Add spaces at the end of the text for scrolling effect
    text_with_spaces = text + ' ' * 16

    for i in range(len(text_with_spaces) - 15):  # Scroll through the text
        lcd.cursor_pos = (0, 0)  # Set cursor to top left corner
        lcd.write_string(text_with_spaces[i:i+16])  # Write the next chunk of text
        time.sleep(0.3)  # Adjust speed of scrolling

# Get IP address and start scrolling
ip = get_wlan0_ip()
status = "my local ip is " + ip
scroll_text(status, lcd)

# Cleanup GPIO settings on exit
GPIO.cleanup()
