import RPi.GPIO as GPIO
from RPLCD import CharLCD
import time
import netifaces

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Initialize the LCD object (16x2 LCD)
lcd = CharLCD(cols=16, rows=2, pin_rs=18, pin_e=23, pins_data=[12, 16, 20, 21],
              numbering_mode=GPIO.BCM)

def get_wlan0_ip():
    """
    Get the IP address associated with 'wlan0'.
    Returns:
        ip (str): IP address if found, otherwise a string indicating failure.
    """
    try:
        # Try fetching the IP address from the 'wlan0' interface
        return netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    except (KeyError, ValueError, IndexError):
        return "No IP address found"
    except Exception as e:
        return f"Error: {str(e)}"

def scroll_text(text, lcd):
    """
    Scroll a given text on the 16x2 LCD.

    Handles `\n` for multiline text. If a 2nd newline appears on the bottom row,
    it clears and starts writing again from the first line.
    
    If a single line text exceeds 16 characters, it will automatically scroll.
    
    Parameters:
        text (str): The string to scroll and display on the LCD.
        lcd (CharLCD): The instance of the CharLCD object.
    """
    lcd.clear()

    # Split the text by newline characters to handle manual line breaks
    lines = text.split('\n')
    
    # Make sure we don't process more than 2 lines (because it's a 2-row LCD)
    while len(lines) > 2:
        lines = lines[:2]  # Too many lines; truncate to just two rows

    # Pad short rows (in case there's only 1 line, or an empty 2nd row)
    if len(lines) == 1:
        lines.append('')  # Add an empty line for the second row
    
    # Ensure each line is padded to 16 characters for full row scrolling
    lines[0] = lines[0].ljust(16)  # First row padded
    lines[1] = lines[1].ljust(16)  # Second row padded

    # Scroll each row if it's too long
    max_scroll_length = max(len(lines[0]), len(lines[1]))  # Biggest scrollable content
    
    # Normalize the lines to at least 16 characters and scroll vertically
    while True:
        for i in range(max_scroll_length - 15):  # Scroll past viewable range (16 - 1 characters)
            lcd.cursor_pos = (0, 0)  # Set the cursor at the top-row (first row)
            lcd.write_string(lines[0][i:i + 16])  # Write first row, scrolling horizontally

            lcd.cursor_pos = (1, 0)  # Set the cursor at the bottom-row (second row)
            lcd.write_string(lines[1][i:i + 16])  # Write the second row text

            # Wait for a while to let the user read before the next scroll
            time.sleep(0.4)
            lcd.clear()

        # Optional: After full scroll, refresh or continue scrolling from row 1.
        time.sleep(1)  # Short pause before repeating or clearing
        break

    lcd.clear()  # Clear the LCD after done

try:
    # Fetch the current WLAN0 IP address
    ip = get_wlan0_ip()

    # Create the message that you want to scroll with a potential line break
    status = "My local\nIP is: " + ip  # Example uses newline to split two rows.
    
    # Scroll the status message across the two-line LCD
    scroll_text(status, lcd)

finally:
    # Cleanup GPIO settings to release all GPIO pins after use
    GPIO.cleanup()
