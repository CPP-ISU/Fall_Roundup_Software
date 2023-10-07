import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="darkcyde15",
  database='pulls'
)

mycursor = mydb.cursor()

##mycursor.execute("CREATE TABLE results (id INT AUTO_INCREMENT PRIMARY KEY, team VARCHAR(255), tractor INT, distance FLOAT(24),speed FLOAT(24))")
sql = "INSERT INTO stock_results (team, tractor, distance, speed) VALUES (%s, %s, %s, %s)"
val = ("Iowa State", 19, 100.34,7.0)
##val = ("South Dakota State", 22, 235.45,9.25)
##val = ("North Dakota State", 23, 175.15,4.25)
mycursor.execute(sql, val)
##mycursor.execute("CREATE TABLE teams (name VARCHAR(255), abbreviation VARCHAR(255),colorR INT, colorG INT, colorB INT)")
mydb.commit()
for x in mycursor:
  print(x) 
