# online imports
import cv2
from pyzbar import pyzbar
import numpy as np
import time
import os
import csv
print("finish online imports")

#onsite imports
import threading
import queue
import sys
print("finish onsite imports")

# online global variables / init
scanned = None
drinkowedLog = {}
owed_file_path = os.path.join(os.path.dirname(__file__), 'owed.csv')    # path to owed.csv GIVEN THEY ARE IN SAME FOLDER
updt_file_path = os.path.join(os.path.dirname(__file__), 'updt.csv')  # path to updt.csv
drink_file_path = os.path.join(os.path.dirname(__file__), 'drinks.csv') # path to drinks.csv
last_logged_num = 0
print("finish online global var")

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

def onsite_join_string(modifying_user_input):
    print(f"onsite_join_string({modifying_user_input})")
    return ''.join(map(str, modifying_user_input))

def onsite_format_user_input(joined_string):
    print(f"onsite_format_user_input({joined_string})")
    return '{:02}'.format(int(joined_string))