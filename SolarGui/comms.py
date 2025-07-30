import serial 
import threading 
import time 
import csv

PORT = 'COM_'  #NEED TO ADD CORRECT PORT
BAUD_RATE = 115200
TIMEOUT = 1
LOG_FILE = 'data_log.csv'

recent_data = {
    'VOC' : None, 
    'TEMP' : None,
    'MPPT' : None, 
}

lock = threading.Lock()
log_enabled = True

def log_to_csv(data)
    with open(LOG_FILE, 'a', newline='') as f: 
        write = csv.writer(f)
        write.writerow([time.time()] + [data.get(k) for k in ['VOC','TEMP','MPPT']])




def parse_line(line):
    global recent_data

    try: 
        fields = line.split('|')
        with lock: 
            for field in fields: 
                if ':' in field: 
                    key, val = field.split(':')
                    key = key.strip().upper()
                    val = int(val.strip())
                    if key in recent_data: 
                        recent_data[key] = val
            if log_enabled: 
                log_to_csv(recent_data)
    except Exception as e: 
        print("Parse error:",e)




def start_serial_read():
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout = TIMEOUT)
        print(f"Opened serial port {PORT} at {BAUD_RATE} baud")
        time.sleep(2)

        with open(LOG_FILE, 'w', newline = '') as f: 
            writer = csv.writer(f)
            writer.writerow(['Time','VOC','TEMP','MPPT'])

        while True: 
            if ser.in_waiting: 
                line = ser.readline().decode(errors = 'replace').strip()
                print("From MCU:", line)
                parse_line(line)

    except serial.SerialException as e: 
        print("Error",e)
    except KeyboardInterrupt: 
        print("Exiting on keyboard interrupt.")
    finally: 
        if 'ser' in locals() and ser.is_open: 
            ser.close()
            print("Serial port closed.")


def get_recent_data():
    with lock: 
        return recent_data.copy()

def start_serial_thread():
    t = threading.Thread(target=serial_thread, daemon = True)
    t.start()