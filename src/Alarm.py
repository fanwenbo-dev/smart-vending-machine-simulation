from hal import hal_buzzer as buz
from hal import hal_ir_sensor as IR
import time

def alarm_activated():
    buz.init()
    buz.beep(0.5, 0.5, 5)

def ir_sensor():
    IR.init()
    state = IR.get_ir_sensor_state()
    return state

def main():
    ir_state = ir_sensor()
    if ir_state == 0:
        alarm_activated()

if __name__ == '__main__':
    main()