import mysql.connector
import dbconnect
cur, con = dbconnect.get_connection()

query = "INSERT INTO tbllanguage (language_code, language_name) VALUES (%s, %s)"
dataset = [('eng', 'English'), ('man', 'Mandarin')]
cur.executemany(query, dataset)
con.commit()