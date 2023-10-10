import serial

# Replace these settings with your camera's configuration
port = 'COM4'
baud_rate = 38400
data_bits = 8
stop_bits = 1
parity = 'N'  # 'N' for None, 'E' for Even, 'O' for Odd

ser = serial.Serial(port, baud_rate, data_bits, parity,stop_bits,timeout=1)

#command=bytes.fromhex('81 01 06 01 18 18 03 01 FF')
for i in range(1):
    #command=bytes.fromhex('81 30 01 FF')
    command=bytes.fromhex('81 01 06 01 18 18 03 02 FF')
    #command=bytes.fromhex('81 2p FF')
    #print(command)
    ser.write(command)
    response = ser.read(size=10)
    print(response)



ser.close()
