import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="darkcyde15",
  database='pulls'
)

mycursor = mydb.cursor()

import csv

# Replace 'your_csv_file.csv' with the actual path to your CSV file
csv_file = r"C:\Users\david\Downloads\IQS_2022_PullData\202206051438_Iowa State.CSV"

with open(csv_file, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file, delimiter=',')

    # Skip the header row if it exists
    next(csv_reader, None)
    next(csv_reader, None)
    # Loop through the rows in the CSV file
    for row in csv_reader:
        # Extract values from the specific columns you want
        timestamp = row[0]
        record_number = int(row[1])
        test_duration = int(row[2])
        school_number = int(row[3])
        load = round(float(row[4]),1)
        pulse_period = float(row[5])
        speed_mph = float(row[6])
        speed_c = float(row[7])
        speed_count = float(row[8])
        dist = float(row[9])
        dist_speed_c = float(row[10])
        dist_speed = float(row[11])
        power1 = float(row[12])
        dist_last = float(row[13])
        pulse_raw = float(row[14])
        pulse_total = float(row[15])

        sql = "INSERT INTO pull_data (pull_num, time, dist, speed, load2) VALUES (%s, %s, %s, %s, %s)"
        val = (1, test_duration, dist,speed_mph, load)
        ##val = ("South Dakota State", 22, 235.45,9.25)
        ##val = ("North Dakota State", 23, 175.15,4.25)
        mycursor.execute(sql, val)
        # Now you can work with the extracted values as needed
        ##print(f"Timestamp: {timestamp}, Record Number: {record_number}, Load: {load}")
    mydb.commit()