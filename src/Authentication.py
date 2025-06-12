import Alarm 

from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
from hal import hal_buzzer as buz
from hal import hal_servo as servo
from hal import hal_adc as adc

from threading import Thread
import RPi.GPIO as GPIO
import time

lcd = LCD.lcd()
lcd.lcd_clear()

val_c = []
user_input = []
valid_code = "*73524"
attempt = 0

GPIO.setmode(GPIO.BCM)      # Set GPIO mode to BCM
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT)    # Configure GPIO26 for PWM
pwm = GPIO.PWM(26, 50)      # Set PWM frequency to 50Hz
pwm.start(3)                # Start PWM with 3% duty cycle
time.sleep(4)
pwm.start(0)
servo_pos = 12

def code(key):
    global user_input
    global val_c
    global attempt
    
    user_input.append(str(key))

    val_c.append("X")
    lcd.lcd_display_string("".join(val_c), 2)

    if len(user_input) == 6:
        entered_code = "".join(user_input)
        if entered_code == valid_code:
            keypad.init(open_door)
        else:
            attempt += 1
            lcd.lcd_clear()
            lcd.lcd_display_string("Invalid Code",  1)
            lcd.lcd_display_string(str(3 - attempt) + " attempts left", 2)

            time.sleep(2)
            user_input.clear()
            val_c.clear()
            lcd.lcd_clear()
            lcd.lcd_display_string("Key user code :", 1)
    
    if attempt >= 3:
        lcd.lcd_clear()
        lcd.lcd_display_string("Too many tries", 1)
        time.sleep(2)
        Alarm.alarm_activated() #Activate alarm


def open_door(key):
    global servo_pos
    pwm.start(servo_pos)
    time.sleep(4)
    if servo_pos == 3:
        servo_pos = 12
    else:
        servo_pos = 3    
    pwm.start(0)

def main():
    # Initialize LCD
    lcd.lcd_clear()
    lcd.lcd_display_string("Key user code :", 1)

    time.sleep(3)

    # Initialize the keypad with the code callback function
    keypad.init(code)

    #Initialize adc
    adc.init()

    #Initialise servo motor
    servo.init()

    # Start keypad listening thread
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.daemon = True  # Ensure the thread exits when the main program does
    keypad_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    main()
