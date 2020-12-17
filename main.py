import serial  # 引用pySerial模組
import time

# db
from db_wrapper import DBWrapper

db = DBWrapper()

COM_PORT = '/dev/ttyACM0'    # 指定通訊埠名稱
BAUD_RATES = 9600    # 設定傳輸速率
ser_tgs = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠

# SDS011
import struct
from datetime import datetime

# Change this to the right port - /dev/tty* on Linux and Mac and COM* on Windows
PORT = '/dev/ttyUSB0'

UNPACK_PAT = '<ccHHHcc'
ser_sds011 =  serial.Serial(PORT, 9600, bytesize=8, parity='N', stopbits=1)

# CCS811
import board
import busio
import adafruit_ccs811

i2c = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c)

# Wait for the sensor to be ready
while not ccs811.data_ready:
    pass
 

while True:
    while ser_tgs.in_waiting:  # 若收到序列資料…
        data_raw = ser_tgs.readline()  # 讀取一行
        if len(data_raw.decode().strip()) > 0:  # 用預設的UTF-8解碼
            tvoc_tgs = int(data_raw.decode().split('\r')[0])
        else:
            continue
        
        # SDS011
        data = ser_sds011.read(10)
        unpacked = struct.unpack(UNPACK_PAT, data)
        ts = datetime.now()
        pm25 = unpacked[2] / 10.0
        pm10 = unpacked[3] / 10.0

        # CCS811
        print("{} TVOC-CCS: {} PPB, TVOC-TGS: {}, PM2.5: {}, PM10: {}".format(ts, ccs811.tvoc, tvoc_tgs, pm25, pm10))
        db.insert_data(ccs811.tvoc, tvoc_tgs, pm25, pm10)
        time.sleep(1)