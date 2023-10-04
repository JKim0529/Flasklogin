from flask import Flask, render_template, request, redirect
import json
import mysql.connector

connection = mysql.connector.connect(host=ADDRESS, port=PORT_NUMBER,
                                     database=DATABASE_NAME,
                                     user=USERNAME,
                                     password=PASSWORD)

cursor = connection.cursor()

app = Flask(__name__)


@app.route("/create",methods=['GET','POST'])
def index():
    

    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        fullname = fullname.title()
        cursor.execute("INSERT INTO `students`(`Full Name`, `Email`) VALUES ('{}','{}')".format(fullname, email))

        connection.commit()

        return redirect('/')

    return render_template("index.html")

@app.route("/")
def students():

    cursor.execute("SELECT * FROM `students`")
    value=cursor.fetchall()
    return render_template("registration.html", data=value,name="Students")


@app.route("/delete",methods=['GET','POST'])
def delete():
    
    if request.method == 'POST':
        fullname = request.form['fullname']
        fullname = fullname.title()
        cursor.execute("DELETE FROM `students` WHERE `Full Name` = '{}'".format(fullname))

        connection.commit()

        return redirect('/students')
    

    return render_template("delete.html")


@app.route("/update")
def update():
    
    return render_template("update.html")


@app.route("/update_name",methods=['GET','POST'])
def update_name():


    if request.method == 'POST':
        oldname = request.form['oldname']
        oldname = oldname.title()
        newname = request.form['newname']
        newname = newname.title()
        cursor.execute("UPDATE `students` SET `Full Name`='{}' WHERE `Full Name` = '{}'".format(newname, oldname))

        connection.commit()

        return redirect('/students')
    
    return render_template("update_name.html")


@app.route("/update_email",methods=['GET','POST'])
def update_email():


    if request.method == 'POST':
        fullname = request.form['fullname']
        fullname = fullname.title()
        new_email = request.form['new_email']
        cursor.execute("UPDATE `students` SET `Email`='{}' WHERE `Full Name` = '{}'".format(new_email, fullname))

        connection.commit()

        return redirect('/students')
    
    return render_template("update_email.html")


@app.route("/processUserInfo/<string:userInfo>",methods=['GET','POST'])
def processUserInfo(userInfo):
    userInfo = json.loads(userInfo)
    print()
    print("USER INFO RECEIVED")
    print('------------------')
    print(f"User Name: {userInfo['name']}")
    print(f"User Type: {userInfo['type']}")
    print()

    return "Info Received Successfully"
    return render_template("test.html", username=userInfo['name'],usertype=userInfo['type'])


if __name__ == "__main__":
    app.run(debug=True)
