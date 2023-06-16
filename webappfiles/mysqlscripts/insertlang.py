import mysql.connector
import dbconnect
cur, con = dbconnect.get_connection()

query = "INSERT INTO tbllanguage (language_code, language_name) VALUES (%s, %s)"
data = ('fre', 'French')
cur.execute(query, data)
con.commit()