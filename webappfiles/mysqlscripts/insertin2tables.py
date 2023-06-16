import mysql.connector
import dbconnect
cur, con = dbconnect.get_connection()

sql = "INSERT INTO tblbook (title, isbn, total_pages, publication_date, price, quantity,instock, book_cover, language_id, genre_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"

val = ('Tom Sawyer', '085656426X', 600, '2018-9-28', 325, 45, 1, 'tom.jpg', 1,2)

cur.execute(sql, val)

con.commit()

print(cur.rowcount, "was inserted and the last id is: ", cur.lastrowid)

sql2 = "INSERT INTO tblbook_author (book_id, author_id) VALUES (%s, %s)"
val2 = (cur.lastrowid,2)
cur.execute(sql2, val2)
con.commit()