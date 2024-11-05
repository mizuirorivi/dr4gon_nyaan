import RPi.GPIO as GPIO
from RPLCD import CharLCD

lcd = CharLCD(cols=16, rows=2, pin_rs=18, pin_e=23, pins_data=[12, 16, 20, 21],
              numbering_mode=GPIO.BCM)
lcd.write_string(u'Hello world!')
