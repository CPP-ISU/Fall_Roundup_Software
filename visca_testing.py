import serial

# Replace these settings with your camera's configuration
port = 'COM4'
baud_rate = 38400
data_bits = 8
stop_bits = 1
parity = 'N'  # 'N' for None, 'E' for Even, 'O' for Odd

ser = serial.Serial(port, baud_rate, data_bits, parity,stop_bits)

command=b'8101060106050101FF'
ser.write(command)
response = ser.readline()
print(response)