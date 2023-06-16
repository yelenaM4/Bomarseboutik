import mysql.connector
import dbconnect

cur, con = dbconnect.get_connection()

cur.execute("SELECT * FROM tbllanguage LIMIT 100 OFFSET 2")

myresult = cur.fetchall()

for x in myresult:
    print(x)