from flask import Flask, render_template,request,redirect
import sqlite3

users_data = {
    "std001": {"password": "10000", "role": "student"},
    "std002": {"password": "20000", "role": "student"},
    "std003": {"password": "30000", "role": "student"},
    "std004": {"password": "40000", "role": "student"},
    "seller001": {"password": "00001", "role": "seller"},
    "seller002": {"password": "00002", "role": "seller"},
    "seller003": {"password": "00003", "role": "seller"}
}

menu = sqlite3.connect("data.db")
Tool = menu.cursor()

Tool.execute("""CREATE TABLE IF NOT EXISTS menu (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             seller_id INTEGER NOT NULL,
             name_menu TEXT NOT NULL,
             price REAL NOT NULL,
             description TEXT NOT NULL
             )
""")

menu.commit()
menu.close()
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('P_Signin.html')
@app.route('/login' , methods=['GET', 'POST'])
def U_P():
    username = request.form['username']
    password = request.form['password']

    if username in users_data:
        if users_data[username]['password'] == password:
            role = users_data[username]['role']
            if role == 'student':
                return redirect('/customer')
            elif role == 'seller':
                return redirect('/seller')
        else:
            return "รหัสผ่านไม่ถูกต้อง"
    else:
        return "ไม่พบบัญชีผู้ใช้"

@app.route('/customer' )
def customer():
    return render_template('store.html')
@app.route('/noodle')
def noodle_page():
    return render_template('noodle.html')

@app.route('/pay')
def pay_page():
    return render_template('pay.html')

@app.route('/order')
def order_page():
    return render_template('order.html')

@app.route('/account')
def account_page():
    return render_template('account.html')

@app.route('/seller')
def menu_page():
    return render_template("main_menu.html")

@app.route('/income')
def income():
    return render_template("income.html")


if __name__ == "__main__":
    app.run()
