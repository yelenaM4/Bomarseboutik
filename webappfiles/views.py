from flask import Blueprint, render_template, request, session, redirect, flash
import emoji
import mysql.connector
from webappfiles import dbconnect
from datetime import datetime
import os


views = Blueprint('views', __name__)

cur, con = dbconnect.get_connection()

#referring to the default page via the “/” route
@views.route("/")
def home():
    emoj = emoji.emojize(":snake:")
    return render_template("index.html", x = emoj)

@views.route("/about/")
def about():
    return render_template("about.html")

@views.route("/adminhome/")
def adminhome():
    return render_template("adminhome.html")

@views.route("/help/")
def help():
    return render_template("help.html")

@views.route("/addbook/")
def add_book():
    cur.execute("select * from tblgenre")
    rows1 = cur.fetchall()
    cur.execute("select * from tbllanguage")
    rows2 = cur.fetchall()
    cur.execute("select * from tblauthor")
    rows3 = cur.fetchall()
    return render_template("addbook.html", rows1 = rows1, rows2 = rows2, rows3 = rows3)

@views.route("/savedetails", methods = ["POST"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            # add codes to retrieve the form values
            title = request.form["txttitle"]
            isbn = request.form["txtisbn"]
            price = request.form["txtprice"]
            qty = request.form["txtqty"]
            numpages = request.form["txtnumpage"]
            genre = request.form["ddlgenre"]
            lang = request.form["ddllang"]
            instk = bool(request.form.get("chkavailable"))
            f = request.files["filecover"]
            f.save(os.path.join("./webappfiles/static/images" , f.filename))
            full_filename = os.path.join("/static/images" , f.filename)
            dt = request.form["txtpdate"]
            sql = "INSERT into tblbook (title, isbn, price, quantity,total_pages, publication_date, genre_id, language_id, book_cover, instock) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # add the form variables for each column
            val = (title, isbn, price, qty, numpages, dt, genre, lang, full_filename, instk)
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " book added"

            authids = request.form.getlist("ddlauthor")
            lastbkid = cur.lastrowid
            for aid in authids:
                sql2 = "INSERT INTO tblbook_author (book_id, author_id) VALUES (%s, %s)"
                val2 = (lastbkid, aid)
                cur.execute(sql2, val2)
                con.commit()

        except Exception as e:
            con.rollback()
            msg = "Book cannot be added " + str(e)
        finally:
            #pass the msg variable to the return statement
            return render_template("addbook.html", msg = msg)
            con.close()

@views.route("/viewbook/")
def view_book():
    cur.execute("SELECT * FROM tblbook bk INNER JOIN tblbook_author bka on \
    (bk.book_id=bka.book_id) \
    INNER JOIN tblauthor auth on (auth.author_id=bka.author_id)")
    rows = cur.fetchall()
    return render_template("viewbooks.html", rows = rows)

@views.route("/searchbook/")
def search_book():
    return render_template("search.html")

@views.route("/updatebook/")
def update_book():
    return render_template("updatebook.html")

@views.route("/deletebook/")
def delete_book():
    return render_template("deletebook.html")

@views.route("/searchcustomer/")
def search_customer():
    return render_template("searchcustomer.html")

@views.route("/manageauthor/")
def manage_author():
    return render_template("manageauthor.html")

@views.route("/searchbk/", methods = ["GET"])
def searchbook():
    #retrieve the querystring txtlang from the URL
    lang = request.args.get("txtlang")
    try:
        sql = "select * from tblbook bk INNER JOIN tbllanguage lg ON \ bk.language_id=lg.language_id WHERE language_name LIKE %s ORDER BY title DESC"
        val = ('%' + lang + '%',)
        cur.execute(sql, val)
        rows = cur.fetchall()
        msg = str(cur.rowcount) + " record found!"
    except:
        msg = "There was an issue while searching!"
    finally:
        return render_template("search.html", msg = msg, rows = rows, lang = lang)

@views.route("/updaterecord/", methods = ["POST"])
def updaterecord():
    #retrieve the form values
    price = request.form["txtprice"]
    isbn = request.form["txtisbn"]
    try:
        sql = "UPDATE tblbook SET price = %s where isbn = %s"
        val = (price, isbn)
        cur.execute(sql, val)
        con.commit()
        msg = str(cur.rowcount) + " record successfully updated"
    except:
        msg = "Cannot be updated"
    finally:
        return render_template("updatebook.html", msg = msg)

@views.route("/deleterecord/", methods = ["POST"])
def deleterecord():
    #retrieve the form value
    isbn = request.form["txtisbn"]
    try:
        sql = "DELETE FROM tblbook WHERE isbn = %s"
        val = (isbn,)
        cur.execute(sql, val)
        con.commit()
        msg = str(cur.rowcount) + " record successfully deleted"
    except:
        msg = "Cannot be deleted"
    finally:
        return render_template("deletebook.html", msg = msg)

@views.route("/profile/")
def profile():
    if 'userid' in session:
        cur, con = dbconnect.get_connection()
        sql = "SELECT * FROM tbluser where user_id = %s"
        val = (session.get('userid'),)
        cur.execute(sql, val)
        rows = cur.fetchall()
        return render_template('profile.html', rows=rows)
    else:
        return redirect('/')

@views.route("/updateprofile/", methods=["GET", "POST"])
def update_profile():
    if request.method == "POST":
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        phone = request.form['txtphone']
        try:
            cur, con = dbconnect.get_connection()
            sql = "UPDATE tbluser SET email = %s, firstname = %s, lastname = %s , phone = %s where user_id = %s"
            val = (email, first_name, last_name, phone, session['userid'])
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " record successfully updated"
            flash(msg, category='success')
        except:
            msg = "Cannot be updated"
            flash(msg, category='error')
        finally:
            return redirect('/profile/')
    else:
        return redirect('/login/')

@views.route("/booklisting/")
def book_listing():
    cur, con = dbconnect.get_connection()
    cur.execute("SELECT * FROM tblbook")
    rows = cur.fetchall()
    return render_template('booklisting.html', rows=rows)