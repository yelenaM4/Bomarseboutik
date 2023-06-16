import mysql.connector
import dbconnect
cur, con = dbconnect.get_connection()

cur.execute("CREATE TABLE tblbook ("
"book_id INTEGER PRIMARY KEY AUTO_INCREMENT, "
"title varchar(300) NOT NULL, "
"isbn varchar(13) NULL, "
"total_pages INT NULL, "
"publication_date date NULL,"
"price decimal(5,2) NOT NULL,"
"quantity INT NOT NULL,"
"InStock TINYINT(1) DEFAULT 0,"
"book_cover varchar(255) NULL)")