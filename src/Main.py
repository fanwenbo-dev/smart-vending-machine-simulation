import RPi.GPIO as GPIO # import RPi.GPIO module
import subprocess       # import subprocess module to run other scripts
from picamera2 import Picamera2, Preview

GPIO.setmode(GPIO.BCM)  # choose BCM mode
#GPIO.setwarnings(False)
GPIO.setup(22, GPIO.IN) # set GPIO 22 as input

#global cam
global global_state 
global_state= False
print(global_state)

def main():
    print(global_state)
    if GPIO.input(22):
        subprocess.run(["python3.9", "Online_Onsite.py"]) # run combine_attempt_2_wocam.py
    else:
        subprocess.run(["python3.9", "Authentication.py"])          # run Authentication.py
    
def cam_value():
    global_state = True
    print(global_state)
    main()

if __name__ == "__main__":
    main()
