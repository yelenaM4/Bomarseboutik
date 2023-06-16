from flask_mail import Mail, Message
from . import mail
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector
from webappfiles import dbconnect
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route("/signup/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        password1 = request.form['txtpwd']
        password2 = request.form['txtcpwd']

        cur, con = dbconnect.get_connection()
        sql = "select email from tbluser where email= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        if (count > 0):
            flash('User already exists.', category='error')
        if (len(email) < 5):
            flash('Email must be greater than 4 characters.', category = 'error')
        elif (len(first_name) < 3):
            flash('First name must be greater than 2 characters.', category = 'error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category = 'error')
        elif (len(password1) < 3):
            flash('Password must be at least 3 characters.', category = 'error')
        else:
            passw = generate_password_hash(password1, method='sha256')
            sql2 = "INSERT into tbluser (email, firstname, lastname, password) values (%s,%s,%s,%s)"
            val2 = (email, first_name, last_name, passw)
            cur.execute(sql2, val2)
            con.commit()
            msg = str(cur.rowcount) + " record added, "

            msg1 = Message('BoMarseBoutik store', sender ='yelenamarion@gmail.com', recipients = [email])
            msg1.body = "Welcome to bomarseboutik store " + first_name + "\r\n"
            msg1.body += "You are now a member and may access the website \r\n "
            msg1.body += "@ http://localhost:5000/"
            mail.send(msg1)

            flash(msg + ' account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html")

@auth.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['txtemail']
        pwd = request.form['txtpwd']

        cur, con = dbconnect.get_connection()
        sql = "select password, email, user_id, firstname from tbluser where email= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount
        for row in rows:
            passw = row[0]

        if (count > 0):
            if check_password_hash(passw, pwd):
                session['userid'] = rows[0][2]
                session['fn'] = rows[0][3]
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.profile'))
        else:
            flash('Incorrect password, pls try again.', category='error')
    else:
        flash('Email does not exist.', category='error')
    return render_template("login.html")

@auth.route('/logout/')
def logout():
    session.pop('userid')
    return redirect('/')