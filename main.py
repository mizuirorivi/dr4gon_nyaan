import RPi.GPIO as GPIO
from RPLCD import CharLCD
import time
import netifaces

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Initialize the LCD object
lcd = CharLCD(cols=16, rows=2, pin_rs=18, pin_e=23, pins_data=[12, 16, 20, 21],
              numbering_mode=GPIO.BCM)

def get_wlan0_ip():
    """
    Get the IP address associated with 'wlan0'.
    Returns:
        ip (str): IP address if found, else a string indicating the failure.
    """
    try:
        # Try fetching the IP address from the 'wlan0' interface
        return netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    except (KeyError, ValueError, IndexError):
        # If there is a problem fetching the IP, return a message
        return "No IP address found for wlan0"
    except Exception as e:
        # Catch generic exceptions just for safety
        return f"Error: {str(e)}"

def scroll_text(text, lcd):
    lcd.clear()    
    text_with_spaces = text.ljust(32)  # Pad the text for smooth scrolling

    # Begin scrolling text on the LCD
    for i in range(len(text_with_spaces) - 31):  # Adjust range for smooth scrolling in a 16-column LCD
        lcd.cursor_pos = (0, 0)  # Set cursor to the top-left corner

    lcd.clear()

try:
    # Fetch the current WLAN0 IP address
    ip = get_wlan0_ip()
    
    # Assemble the message to be displayed and scrolled on the LCD
    status = "My local IP is \n" + ip
    
    # Scroll the message text across the LCD
    scroll_text(status, lcd)

finally:
    # Cleanup GPIO settings to release all GPIO pins after use
    GPIO.cleanup()
