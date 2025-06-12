import time
from threading import Thread
import queue
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad

#Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()

#Call back function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)

def main():
    print("entering inactive state")
    time.sleep(3)
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()
    lcd = LCD.lcd()
    lcd.lcd_clear()
    lcd.backlight(0)
    while True:
        keyvalue= shared_keypad_queue.get()

        if keyvalue:
            lcd.backlight(1)
            print("i awaoke")
            break



if __name__ == '__main__':
    main()