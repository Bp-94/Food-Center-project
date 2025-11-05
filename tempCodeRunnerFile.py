import os
from flask import Flask, render_template,request,redirect
import sqlite3
from werkzeug.utils import secure_filename

users_data = {
    "std001": {"password": "10000", "role": "student"},
    "std002": {"password": "20000", "role": "student"},
    "std003": {"password": "30000", "role": "student"},
    "std004": {"password": "40000", "role": "student"},
    "seller001": {"password": "00001", "role": "seller","shop_name": "ร้านก๋วยเตี๋ยว"},
    "seller002": {"password": "00002", "role": "seller","shop_name": "ร้านข้าวหมูแดงหมูกรอบ"},
    "seller003": {"password": "00003", "role": "seller","shop_name": "ร้านข้าวมันไก่"}
}

menus = sqlite3.connect("data.db")
Tool = menus.cursor()

Tool.execute("""
            CREATE TABLE IF NOT EXISTS menus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_name TEXT NOT NULL,
            menu_name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            image TEXT
)
""")

menus.commit()
menus.close()
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def login_page():
    return render_template('P_Signin.html')

@app.route('/login', methods=['POST'])
def U_P():
    username = request.form['username']
    password = request.form['password']

    if username in users_data:
        if users_data[username]['password'] == password:
            role = users_data[username]['role']
            if role == 'student':
                return redirect('/shops')
            elif role == 'seller':
                shop_name = users_data[username]['shop_name']
                return redirect(f'/seller?shop_name={shop_name}')
        else:
            return "รหัสผ่านไม่ถูกต้อง"
    else:
        return "ไม่พบบัญชีผู้ใช้"
    return render_template('P_Signin.html')

@app.route('/foodform', methods=['GET', 'POST'])
def foodform():
    if request.method == 'POST':
        menu_name = request.form['menu_name']
        shop_name = request.form['shop_name']
        price = request.form['price']
        description = request.form['description']
        image = request.files['image']
        image_filename = None

        # --- จัดการไฟล์รูป ---
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_filename = filename

        # --- บันทึกข้อมูลลงฐานข้อมูล ---
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO menus (shop_name, menu_name, price, description, image)
            VALUES (?, ?, ?, ?, ?)
        """, (shop_name, menu_name, price, description, image_filename))
        conn.commit()

        # --- ดึงข้อมูลเมนูทั้งหมดของร้านนั้น ---
        c.execute("SELECT menu_name, price, description, image FROM menus WHERE shop_name = ?", (shop_name,))
        menus = c.fetchall()
        conn.close()

        return redirect(f'/seller?shop_name={shop_name}')
    else:
        shop_name = request.args.get('shop_name')
        return render_template('foodform.html', shop_name=shop_name)

@app.route('/seller')
def menu_page():
    shop_name = request.args.get('shop_name')
    return render_template('main_menu.html' , shop_name=shop_name)

@app.route("/shop")
def shop():
    shop_name = request.args.get("shop_name")
    shop_image = request.args.get("shop_image")
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT menu_name, price, description, image FROM menus WHERE shop_name=?", (shop_name,))
    menus = c.fetchall()
    conn.close()
    return render_template("shop.html", shop_name=shop_name, menus=menus,shop_image=shop_image)


@app.route('/shops')
def shops_page():
    return render_template('shops.html')
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


@app.route('/income')
def income():
    return render_template("income.html")



if __name__ == "__main__":
    app.run(debug=True)
