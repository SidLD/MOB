from flask import Blueprint, redirect, render_template, request, session,url_for
auth = Blueprint('auth',__name__)
from . import mysql

@auth.route('/login',methods=['GET','POST'])
def login():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        uname = request.form['uname']
        psw = request.form['psw']
        resultValue = cur.execute("Select * FROM t_user WHERE user_name=%s AND user_password=%s AND user_type='user'",(uname,psw))
        resultValue = cur.fetchone()
        if resultValue:
            session['loggedin'] = True
            session['user_id'] = resultValue[0]
            session['username'] = resultValue[3]
            if resultValue[5]=='user':
                return redirect(url_for("views.index"))
        else:
            return render_template("login.html")
    else:
        if 'username' and 'user_id' in session:
            return redirect(url_for("views.index"))
        return render_template("login.html")

@auth.route('/register',methods=['GET','POST'])
def register():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        uname = request.form['uname']
        psw = request.form['psw']
        user_type  = "user"
        cur.execute(""" INSERT INTO 
                    t_user (firstname,lastname,user_name,user_password,user_type) 
                    VALUES (%s,%s,%s,%s,%s) """,(fname,lname,uname,psw,user_type))
        mysql.connection.commit()
        return redirect(url_for("auth.login"))
    return render_template("sign-up.html")
    
@auth.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('user_id',None)
    session.pop('username',None)
    return redirect(url_for("views.index"))