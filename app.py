from flask import Flask,render_template,request,redirect,url_for
import sqlite3 as sql

app=Flask(__name__)


@app.route("/")
def home():
     conn = sql.connect("crud.db")
     conn.row_factory=sql.Row
     cur=conn.cursor()
     cur.execute("select * from users")
     data=cur.fetchall()
     return render_template("home.html",datas=data)

@app.route("/adduser",methods=["GET","POST"])
def adduser():
    if request.method=="POST":
        s_name=request.form['name']
        s_age=request.form['age']
        s_location=request.form['location']
        s_language=request.form['language']
        conn = sql.connect("crud.db")
        cur=conn.cursor()
        cur.execute("insert into users (NAME,AGE,LOCATION,LANGUAGE) values(?,?,?,?)",(s_name,s_age,s_location,s_language))
        conn.commit()
        return redirect(url_for("home"))
        # return render_template("home.html")
    return render_template("add_user.html")

@app.route("/edituser/<string:id>",methods=["GET","POST"])
def edituser(id):
    if request.method=="POST":
        s_name=request.form['name']
        s_age=request.form['age']
        s_location=request.form['location']
        s_language=request.form['language'] 
        conn = sql.connect("crud.db")
        cur=conn.cursor()
        cur.execute("update users set NAME=?,AGE=?,LOCATION=?,LANGUAGE=? where ID=?",(s_name,s_age,s_location,s_language,id))            
        conn.commit()
        return redirect(url_for("home"))
    conn=sql.connect("crud.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("select * from users where ID=?",(id,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)

@app.route("/deleteuser/<string:id>",methods=["GET"])
def deleteuser(id):
    conn=sql.connect("crud.db")
    cur=conn.cursor()
    cur.execute(" delete from  users where ID=?",(id,))
    conn.commit()
    return redirect(url_for("home"))



if __name__=="__main__":
    app.run(debug=True)