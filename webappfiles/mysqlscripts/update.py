import mysql.connector
import dbconnect
cur, con = dbconnect.get_connection()

sql = "UPDATE tblbook SET total_pages = 495 WHERE title = 'Dubliners'"

cur.execute(sql)

con.commit()

print(cur.rowcount, "record(s) affected")