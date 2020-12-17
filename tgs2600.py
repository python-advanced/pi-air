import serial  # 引用pySerial模組
import time

COM_PORT = '/dev/ttyACM0'    # 指定通訊埠名稱
BAUD_RATES = 9600    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠

while True:
    while ser.in_waiting:  # 若收到序列資料…
        data_raw = ser.readline()  # 讀取一行
        if len(data_raw.decode().strip()) > 0:  # 用預設的UTF-8解碼
            tvoc = int(data_raw.decode().split('\r')[0])
        else:
            continue

        print("TGS-TVOC: {}".format(tvoc))
        time.sleep(1)
