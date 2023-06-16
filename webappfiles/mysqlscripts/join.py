import mysql.connector
import dbconnect
cur, con = dbconnect.get_connection()

sql = "SELECT \
book.title, \
language.language_name \
FROM tblbook book \
INNER JOIN tbllanguage language ON book.language_id = language.language_id "

cur.execute(sql)

myresult = cur.fetchall()

for x in myresult:
    print(x)