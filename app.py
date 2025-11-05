import os
from flask import Flask, render_template,request,redirect
import sqlite3
from werkzeug.utils import secure_filename

users_data = {
    "std001": {"password": "10000", "role": "student"},
    "std002": {"password": "20000", "role": "student"},
    "std003": {"password": "30000", "role": "student"},
    "std004": {"password": "40000", "role": "student"},
    "seller001": {"password": "00001", "role": "seller,","shop_name": "ร้านก๋วยเตี๋ยว"},
    "seller002": {"password": "00002", "role": "seller","shop_name": "ร้านโคเจ"},
    "seller003": {"password": "00003", "role": "seller","shop_name": "ร้านข้าวมันไก่"}
}

menu = sqlite3.connect("data.db")
Tool = menu.cursor()

Tool.execute("""CREATE TABLE IF NOT EXISTS menu (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             menu_name TEXT NOT NULL,
             price REAL NOT NULL,
             description TEXT NOT NULL,
             image TEXT
             )
""")

menu.commit()
menu.close()
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
                shop_name = users_data[username]['shop_name']
                return redirect(f'/seller?shop_name={shop_name}')
        else:
            return "รหัสผ่านไม่ถูกต้อง"
    else:
        return "ไม่พบบัญชีผู้ใช้"
@app.route('/foodform')
def foodform():
    if request.method == 'POST':
        menu_name = request.form('menu_name')
        shop_name = request.form('shop_name')
        price = request.form('price')
        description = request.form('description')
        image = request.files['image']
        image_filename = None
        if image and image.filename != '':
                # ป้องกันชื่อไฟล์อันตราย
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_filename = filename

        # ✅ บันทึกข้อมูลลงฐานข้อมูล
        conn = sqlite3.connect('menus.db')
        c = conn.cursor()
        c.execute("""INSERT INTO menus (shop_name, menu_name, price, description, image)
                        VALUES (?, ?, ?, ?, ?)""",
                    (shop_name, menu_name, price, description, image_filename))
        conn.commit()
        conn.close()

        if shop_name == "ร้านก๋วยเตี๋ยว":
            return redirect
        return redirect(f'/shop/{shop_name}')
    else:
        shop_name = request.args.get('shop_name')
        return render_template('foodform.html', shop_name=shop_name)

@app.route('/noodle')
def noodle_page():
    return render_template('noodle.html')

@app.route('/koje')
def koje_page():
    return render_template('koje_store.html')

@app.route('/kaomankai')
def kaomanki_page():
    return render_template('kaomankai_store.html')
@app.route('/pay')
def pay_page():
    return render_template('pay.html')

@app.route('/order')
def order_page():
    return render_template('order.html')
@app.route('/customer' )
def customer():
    return render_template('store.html')

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
    app.run(debug=True)
