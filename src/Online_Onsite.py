import RPi.GPIO as GPIO
# online imports
from picamera2 import Picamera2, Preview
import cv2
from pyzbar import pyzbar
import numpy as np
import time
import os
import csv
from hal import hal_lcd as LCD
print("finish online imports")

import inactive
import Main as mainfile


# onsite imports
import threading
from hal import hal_keypad as keypad
from hal import hal_rfid_reader as rfid_reader
import queue
print("finish onsite imports")

# online global variables / init
scanned = None
drinkowedLog = {}
owed_file_path = os.path.join(os.path.dirname(__file__), 'owed.csv')    # path to owed.csv GIVEN THEY ARE IN SAME FOLDER
updt_file_path = os.path.join(os.path.dirname(__file__), 'updt.csv')    # path to updt.csv
drink_file_path = os.path.join(os.path.dirname(__file__), 'drinks.csv') # path to drinks.csv
last_logged_num = 0
print("finish online global var 1")




print("why am i running")
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)
print("finish online global var 2")


# onsite global variables / init
user_input = []
allow_rfid_scan = False
inactivity_timeout = 15
inactivity_timer = None
transaction_complete = False
reader = None
keypad_thread = None
rfid_thread = None
running = False
print("finish onsite global var")

onsite_flag = False
shared_keypad_queue = queue.Queue()

def overall_key_pressed(key):
    if onsite_flag: onsite_key_pressed(key)
    else: main_key_pressed(key)
keypad.init(overall_key_pressed)
overall_keypad_thread = threading.Thread(target=keypad.get_key)
overall_keypad_thread.daemon = True
overall_keypad_thread.start()
lcd = LCD.lcd()
print("finish overall global var")

# online funtions
def online_extract_decoded_data(decoded_list):
    print(f"online_extract_decoded_data({decoded_list})")
    try: decoded_data = decoded_list[0].data.decode('utf-8')
    except: decoded_data = None
    print(decoded_data, "detected")
    return decoded_data

def online_get_qrstring_drinkno(qr):
    print(f"online_get_qrstring_drinkno({qr})")
    qr_string_decode = {
        '2a0201': 1,
        '2a0202': 2,
        '2a0203': 3,
        '2a0204': 4,
        '2a0205': 5,
        '2a0206': 6,
        '2a0207': 7,
        '2a0208': 8,
        '2a0209': 9,
        '2a0210': 10
    }
    try: temp = qr_string_decode[str(qr)]
    except: temp = 0
    return temp

def online_decode_qr(frame):
    print(f"online_decode_qr({frame})")
    # decode qr
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        points = obj.polygon    # draw rect
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        for j in range(0, n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)
    return frame, decoded_objects

def online_checkdrinksowed(number):
    print(f"online_checkdrinksowed({number})")
    global drinkowedLog
    return drinkowedLog[int(number)]

def online_finddrinkinfo(find, value):
    print(f"online_finddrinkinfo({find}, {value})")
    drinkinfo = []
    with open(drink_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        drinkinfo = list(reader)
    for drink in drinkinfo:
        if drink['index'] == str(value):
            if find == 'name':
                return drink['drink']
            elif find == 'price':
                return drink['price'].strip()
    return None  # Return None if index not found

def online_getNewcsv():
    print("online_getNewcsv()")
    with open(updt_file_path, mode='r', newline='') as file: # csv file read
        reader = csv.DictReader(file)
        rows = list(reader)
    return rows

def online_getdrinksowed():
    print("online_getdrinksowed()")
    global drinkowedLog
    with open(owed_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for i in rows:
        try: drinkowedLog[int(i['drinknumber'])] = int(i['value'])
        except: drinkowedLog[str(i['drinknumber'])] = int(i['value'])

def online_writedrinksowed():
    print("online_writedrinksowed()")
    global owed_file_path
    global drinkowedLog
    with open(owed_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['drinknumber', 'value'])
        for drinknumber, value in drinkowedLog.items():
            writer.writerow([drinknumber, value])

def online_fetchnew():
    print("online_fetchnew()")
    online_getdrinksowed()
    global last_logged_num
    last_logged_num = drinkowedLog['last_updt']
    retrieved = online_getNewcsv()
    if retrieved == []: last_logged_num = 0
    else:
        diff = int(retrieved[-1]['number']) - last_logged_num
        while diff > 0 :
            drinkname = online_finddrinkinfo('name', int(retrieved[-abs(diff)]['drink']))
            print("writing", drinkname, "ordered at", retrieved[-abs(diff)]['date'], retrieved[-abs(diff)]['time'])
            drinkowedLog[int(retrieved[-abs(diff)]['drink'])] += 1
            diff -= 1
            time.sleep(1)
        last_logged_num = int(retrieved[-1]['number'])
    drinkowedLog['last_updt'] = last_logged_num
    online_writedrinksowed()  

def online_main(): # called on when key press is 2 in main
    print("online_main()")
        
    online_fetchnew()
    global scanned
    picam2.start_preview(Preview.QTGL)  # Start the camera preview
    picam2.start()
    lcd.lcd_clear()
    lcd.lcd_display_string("Scan given QR:", 1)
    tries = 60
    try:
        while tries > 0:
            frame = picam2.capture_array()  # Capture a frame
            frame, decoded_objects = online_decode_qr(frame)   # Decode the QR codes in the frame
            cv2.imshow("QR Code Scanner", frame)    # Display the frame with decoded QR codes
            tries -= 1
            print("tries decreased by 1")
            print(f"Tries = {tries}")
            if decoded_objects: # Check if any QR code is detected
                lcd.lcd_display_string("QR code detected", 1)
                scanned = online_extract_decoded_data(decoded_objects)
                break

    finally:    # Stop the camera and close the window
        picam2.stop_preview()
        picam2.stop()
        cv2.destroyAllWindows()
    drinkno = online_get_qrstring_drinkno(scanned)
    lcd.lcd_clear()
    if drinkno != 0:
        online_getdrinksowed()
        if online_checkdrinksowed(int(drinkno)) != 0:  # if that drink does have a record purchased online
            global drinkowedLog # increment down drink owed value
            drinkowedLog[int(drinkno)] = drinkowedLog[int(drinkno)] - 1
            online_writedrinksowed()
            lcd.lcd_display_string("Thank you for", 1)
            lcd.lcd_display_string("your purchase", 2)
        else:   # no record of that drink purchased online
            lcd.lcd_display_string("Fraud detected", 1)
            lcd.lcd_display_string("Found no record", 2)
    else:   # invalid QR
        lcd.lcd_display_string("Invalid QR code", 1)
    print("fucking cam")
    scanned = None
    time.sleep(1)

# onsite funct
def onsite_join_string(modifying_user_input):
    print(f"onsite_join_string({modifying_user_input})")
    return ''.join(map(str, modifying_user_input))

def onsite_format_user_input(joined_string):
    print(f"onsite_format_user_input({joined_string})")
    return '{:02}'.format(int(joined_string))

def onsite_key_pressed(key):
    print(f"onsite_key_pressed({key})")
    global user_input, allow_rfid_scan, transaction_complete
    print("Key pressed:", key)
    onsite_reset_inactivity_timer()

    if key in range(10):
        if len(user_input) < 2:
            user_input.append(key)
            lcd.lcd_clear()
            time.sleep(0.1)
            lcd.lcd_display_string("Enter Number:", 1)
            time.sleep(0.1)
            lcd.lcd_display_string(f"{onsite_join_string(user_input)}", 2)
            time.sleep(0.1)
    elif key == '#':
        lcd.lcd_clear()
        time.sleep(0.1)
        joined_string = onsite_join_string(user_input)
        formatted_user_input = onsite_format_user_input(joined_string)

        drink_name = online_finddrinkinfo('name', formatted_user_input)
        drink_price = online_finddrinkinfo('price', formatted_user_input)

        if drink_name and drink_price:
            allow_rfid_scan = True
            lcd.lcd_display_string("Scan to pay", 1, 2)
            time.sleep(1)
            lcd.lcd_clear()
            time.sleep(0.1)
            lcd.lcd_display_string(drink_name, 1, 2)
            time.sleep(0.1)
            lcd.lcd_display_string(drink_price, 2, 2)
            time.sleep(0.1)
        else:
            allow_rfid_scan = False
            lcd.lcd_display_string("No such drink")
            time.sleep(0.1)
            user_input.clear()
    elif key == '*':
        onsite_delete_last_digit()

def onsite_delete_last_digit():
    print("onsite_delete_last_digit()")
    global user_input
    if user_input:
        user_input.pop()
        lcd.lcd_clear()
        time.sleep(0.1)
        if user_input:
            lcd.lcd_display_string("Enter Number:", 1)
            time.sleep(0.1)
            lcd.lcd_display_string(f"{onsite_join_string(user_input)}", 2)
            time.sleep(0.1)
        else:
            lcd.lcd_display_string("Enter Number:", 1)
            time.sleep(0.1)
            lcd.lcd_display_string(" ", 2)
            time.sleep(0.1)

def onsite_rfid_scan_thread():
    print("onsite_rfid_scan_thread()")
    global allow_rfid_scan, transaction_complete, user_input
    while True:
        id = reader.read_id_no_block()
        if id is not None and allow_rfid_scan:
            onsite_reset_inactivity_timer()
            lcd.lcd_clear()
            lcd.lcd_display_string("Dispensing", 2)
            time.sleep(2)
            allow_rfid_scan = False
            user_input.clear()
            transaction_complete = True
            break
        time.sleep(0.1)

def onsite_inactivity_timeout_callback():
    print("onsite_inactivity_timeout_callback()")
    global allow_rfid_scan, user_input, transaction_complete, running
    allow_rfid_scan = False
    user_input.clear()
    lcd.lcd_clear()
    inactive.main()
    lcd.lcd_display_string("Returning to", 1, 2)
    time.sleep(0.1)
    lcd.lcd_display_string("Menu", 2, 2)
    time.sleep(0.1)
    transaction_complete = True
    running = False

def onsite_reset_inactivity_timer():
    print("onsite_reset_inactivity_timer()")
    global inactivity_timer
    if inactivity_timer:
        inactivity_timer.cancel()
    onsite_start_inactivity_timer()

def onsite_start_inactivity_timer():
    print("onsite_start_inactivity_timer()")
    global inactivity_timer
    inactivity_timer = threading.Timer(inactivity_timeout, onsite_inactivity_timeout_callback)
    inactivity_timer.start()

def onsite_run():
    print("onsite_run()")
    global lcd, reader, keypad_thread, rfid_thread, running
    lcd = LCD.lcd()
    lcd.lcd_clear()
    time.sleep(0.1)
    lcd.lcd_display_string("Select", 1, 2)
    time.sleep(0.1)
    lcd.lcd_display_string("Drink :", 2, 2)
    time.sleep(0.1)
    reader = rfid_reader.init()
    onsite_start_inactivity_timer()
    keypad.init(onsite_key_pressed)
    keypad_thread = threading.Thread(target=keypad.get_key)
    keypad_thread.daemon = True
    keypad_thread.start()
    rfid_thread = threading.Thread(target=onsite_rfid_scan_thread)
    rfid_thread.daemon = True
    rfid_thread.start()
    running = True

def onsite_stop():
    print("onsite_stop()")
    global inactivity_timer, running
    print("global inactivity_timer, running")
    try:
        if inactivity_timer:
            print("if inactivity_timer:")
            inactivity_timer.cancel()
            print("inactivity_timer.cancel()")
        running = False
        print("running = False")
        if rfid_thread:
            rfid_thread.join()
            print("rfid stopped")
        if keypad_thread:
            if keypad_thread.is_alive():
                keypad.stop()
                keypad_thread.join()
                print("keypad stopped")
            else:
                print("not running")
    except Exception as e:
        print(f"Error in onsite_stop:{e}")
    print("Threads should be stopped")

def onsite_main():
    print("onsite_main()")
    global running, transaction_complete
    onsite_run()
    while running:
        if transaction_complete:
            lcd.lcd_clear()
            time.sleep(0.1)
            lcd.lcd_display_string("Thank You", 1, 2)
            time.sleep(1)
            lcd.lcd_display_string("Now Resetting", 2, 2)
            time.sleep(0.1)
            print('Returning to menu')
            onsite_stop()
            print("returned to main")
        time.sleep(1)

# main implementation
def main():
    print("main()")
    lcd.lcd_clear()
    lcd.lcd_display_string("1: Key Selection", 1)
    lcd.lcd_display_string("2: Online Payment", 2)
    print("starting to wait for key")
    while True:
        keyvalue= shared_keypad_queue.get()
        print("key value ", keyvalue)
        if keyvalue != None:
            overall_key_pressed(keyvalue)
            break
            
    if overall_keypad_thread:
        if overall_keypad_thread.is_alive():
            print("wait for thread to finish")
            keypad.stop()
            overall_keypad_thread.join()
            print("key stopped")
        else:
            print("not running")
                
    time.sleep(1)

def main_key_pressed(key):
    print(f"overall_key_pressed({key})")
    if key == 1:
        lcd.lcd_clear()
        lcd.lcd_display_string("Onsite Order", 1)
        # Call onsite main function
        onsite_main()
        print("At main")
        mainfile.cam_value()
        #print("i'm trying exit at main_key_pressed")
        #exit()
    elif key == 2:
        lcd.lcd_clear()
        lcd.lcd_display_string("Online Order", 1)
        # Call online main function
        online_main()
        print("At main")
        mainfile.cam_value()
    #print("i'm trying exit aft elif")
    #exit()

if __name__ == "__main__":
    main()
