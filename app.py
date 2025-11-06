import os , uuid
from flask import Flask, render_template,request,redirect, url_for,session
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
Tool_menu = menus.cursor()

Tool_menu.execute("""
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

payment_method = sqlite3.connect("data.db")
Tool_payment = payment_method.cursor()
Tool_payment.execute("""
CREATE TABLE IF NOT EXISTS payment_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_name TEXT NOT NULL,

    cash INTEGER DEFAULT 0,
    promptpay INTEGER DEFAULT 0,
    truemoney INTEGER DEFAULT 0,
    bank_account_enabled INTEGER DEFAULT 0,

    promptpay_number TEXT,
    promptpay_qr TEXT,

    truemoney_number TEXT,

    bank_account_number TEXT,
    bank_name TEXT
);
""")
payment_method.commit()
payment_method.close()

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
            session['username'] = username  

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
            ext = os.path.splitext(secure_filename(image.filename))[1]
            unique_name = f"{shop_name}_{menu_name}_{uuid.uuid4().hex}{ext}"
            unique_name = secure_filename(unique_name)  
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            image.save(image_path)
            image_filename = unique_name

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO menus (shop_name, menu_name, price, description, image)
            VALUES (?, ?, ?, ?, ?)
        """, (shop_name, menu_name, price, description, image_filename))
        conn.commit()


        c.execute("SELECT menu_name, price, description, image FROM menus WHERE shop_name = ?", (shop_name,))
        menus = c.fetchall()
        conn.close()

        return redirect(f'/seller?shop_name={shop_name}')
    else:
        shop_name = request.args.get('shop_name')
        return render_template('foodform.html', shop_name=shop_name)

@app.route('/payment')
def payment_page():
    shop_name = request.args.get('shop_name')
    done = request.args.get('done')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""
        SELECT cash, promptpay, truemoney, bank_account_enabled
        FROM payment_methods
        WHERE shop_name = ?
    """, (shop_name,))
    result = c.fetchone()
    conn.close()

    if result:
        payment_status = {
            'cash': bool(result[0]),
            'promptpay': bool(result[1]),
            'truemoney': bool(result[2]),
            'bank': bool(result[3])
        }
    else:
        payment_status = {'cash': False, 'promptpay': False, 'truemoney': False, 'bank': False}

    if done == 'promptpay':
        return redirect(url_for('promptpay_page', shop_name=shop_name))
    elif done == 'cash':
        return redirect(url_for('cash_page', shop_name=shop_name))
    elif done == 'truemoney':
        return redirect(url_for('truemoney_page', shop_name=shop_name))
    elif done == 'bank':
        return redirect(url_for('bank_account_page', shop_name=shop_name))


    return render_template('payment.html', shop_name=shop_name, result=result ,payment_status = payment_status)
@app.route('/promptpay', methods=['GET'])
def promptpay_page():
    shop_name = request.args.get('shop_name')
    return render_template('Promptpay.html', shop_name=shop_name)

@app.route('/save-promptpay-qr', methods=['POST'])
def save_promptpay():
    shop_name = request.form['shop_name']
    promptpay_number = request.form.get('promptpay_number')
    qr_file = request.files.get('qr_code_image')
    
    qr_filename = None
    if qr_file and qr_file.filename != '':
        # --- ปรับปรุงการตั้งชื่อไฟล์ให้ไม่ซ้ำกัน ---
        ext = os.path.splitext(secure_filename(qr_file.filename))[1]
        unique_name = f"{shop_name}_promptpay_qr_{uuid.uuid4().hex}{ext}"
        qr_filename = secure_filename(unique_name) # ป้องกันอีกชั้น
        qr_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_filename)
        qr_file.save(qr_path)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # --- โลจิกที่แก้ไขแล้ว: ตรวจสอบก่อน ถ้ามีแถวอยู่แล้วให้อัปเดต ---
    c.execute("SELECT id FROM payment_methods WHERE shop_name = ?", (shop_name,))
    exists = c.fetchone()

    if exists:
        # ถ้ามีข้อมูลร้านค้านี้อยู่แล้ว -> UPDATE
        c.execute("""
            UPDATE payment_methods
            SET promptpay = 1,
                promptpay_number = ?,
                promptpay_qr = ?
            WHERE shop_name = ?
        """, (promptpay_number, qr_filename, shop_name))
    else:
        # ถ้ายังไม่มีข้อมูลร้านค้านี้ -> INSERT
        c.execute("""
            INSERT INTO payment_methods 
            (shop_name, promptpay, promptpay_number, promptpay_qr)
            VALUES (?, 1, ?, ?)
        """, (shop_name, promptpay_number, qr_filename))
    # --- จบส่วนที่แก้ไข ---

    conn.commit()
    conn.close()

    # --- คำแนะนำเพิ่มเติม ---
    # เปลี่ยนจาก redirect ไปหน้า 'menu_page' (หน้าหลัก seller)
    # เป็น redirect กลับไปหน้า 'payment_page' (หน้าวิธีการชำระเงิน)
    # จะทำให้ผู้ใช้เห็นผลลัพธ์ที่อัปเดตแล้วทันที
    
    # return redirect(url_for('menu_page', shop_name=shop_name)) # <--- ของเดิม
    return redirect(url_for('payment_page', shop_name=shop_name))
@app.route('/truemoney', methods=['GET', 'POST'])
def truemoney_page():
    shop_name = request.args.get('shop_name') or request.form.get('shop_name')

    if request.method == 'POST':
        truemoney_number = request.form.get('TrueMoney_Wallet_number')

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT id FROM payment_methods WHERE shop_name=?", (shop_name,))
        exists = c.fetchone()
        if exists:
            c.execute("""
                UPDATE payment_methods
                SET truemoney = 1,
                    truemoney_number = ?
                WHERE shop_name = ?
            """, (truemoney_number, shop_name))
        else:
            c.execute("""
                INSERT INTO payment_methods (shop_name, truemoney, truemoney_number)
                VALUES (?, 1, ?)
            """, (shop_name, truemoney_number))
        conn.commit()
        conn.close()
        return redirect(url_for('menu_page') + f'?shop_name={shop_name}')

    return render_template('Truewallet.html', shop_name=shop_name)


@app.route('/cash', methods=['GET', 'POST'])
def cash_page():
    shop_name = request.args.get('shop_name') or request.form.get('shop_name')

    if request.method == 'POST':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT id FROM payment_methods WHERE shop_name=?", (shop_name,))
        exists = c.fetchone()
        if exists:
            c.execute("UPDATE payment_methods SET cash = 1 WHERE shop_name = ?", (shop_name,))
        else:
            c.execute("INSERT INTO payment_methods (shop_name, cash) VALUES (?, 1)", (shop_name,))
        conn.commit()
        conn.close()
        return redirect(url_for('menu_page') + f'?shop_name={shop_name}')

    return render_template('cash.html', shop_name=shop_name)
@app.route('/bank_account', methods=['GET', 'POST'])
def bank_account_page():
    shop_name = request.args.get('shop_name') or request.form.get('shop_name')

    if request.method == 'POST':
        bank_name = request.form['bank_name']
        bank_account_number = request.form['bank_account_number']

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT id FROM payment_methods WHERE shop_name=?", (shop_name,))
        exists = c.fetchone()
        if exists:
            c.execute("""
                UPDATE payment_methods
                SET bank_account_enabled = 1,
                    bank_name = ?,
                    bank_account_number = ?
                WHERE shop_name = ?
            """, (bank_name, bank_account_number, shop_name))
        else:
            c.execute("""
                INSERT INTO payment_methods
                (shop_name, bank_account_enabled, bank_name, bank_account_number)
                VALUES (?, 1, ?, ?)
            """, (shop_name, bank_name, bank_account_number))
        conn.commit()
        conn.close()

        return redirect(url_for('menu_page', shop_name=shop_name, done='bank'))

    return render_template('accountnum.html', shop_name=shop_name)

@app.route('/shops')
def shops_page():
    return render_template('shops.html')

@app.route('/order_payment', methods=['GET', 'POST'])
def order_payment():
    shop_name = request.args.get('shop_name')
    menu_name = request.args.get('menu_name')
    price = request.args.get('price')
    

    username = session.get('username', 'guest')

    # ดึงข้อมูลการชำระเงินของร้านจากฐานข้อมูล
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""
        SELECT cash, promptpay, truemoney, bank_account_enabled,
               promptpay_number, truemoney_number, bank_name, bank_account_number
        FROM payment_methods
        WHERE shop_name = ?
    """, (shop_name,))
    payment_info = c.fetchone()
    conn.close()

    # แปลงข้อมูลให้อ่านง่ายในฝั่ง template
    payment_status = {
        'cash': bool(payment_info[0]) if payment_info else False,
        'promptpay': bool(payment_info[1]) if payment_info else False,
        'truemoney': bool(payment_info[2]) if payment_info else False,
        'bank': bool(payment_info[3]) if payment_info else False,
    }

    return render_template(
        'pay_Store.html',
        shop_name=shop_name,
        menu_name=menu_name,
        price=price,
        username=username,
        payment_status=payment_status,
    )


@app.route('/pay_confirm', methods=['POST'])
def pay_confirm():
    username = request.form['username']
    menu_name = request.form['menu_name']
    price = request.form['price']
    shop_name = request.form.get('shop_name')
    method = request.form['method']  # promptpay / truemoney / cash / bank

    if method == 'promptpay':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT promptpay_number, promptpay_qr FROM payment_methods WHERE shop_name=?", (shop_name,))
        result = c.fetchone()
        conn.close()
        promptpay_number = result[0] if result else 'ไม่พบข้อมูลร้านค้า'
        promptpay_qr_filename = result[1] if result else None

        return render_template('promtpay_confirm.html', username=username, menu_name=menu_name, price=price , promptpay_number = promptpay_number , promptpay_qr_filename=promptpay_qr_filename)
    elif method == 'truemoney':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT truemoney_number FROM payment_methods WHERE shop_name=?", (shop_name,))
        result = c.fetchone()
        conn.close()
        truemoney_number = result[0] if result else 'ไม่พบข้อมูลร้านค้า'

        return render_template('Truewallet_confirm.html', username=username, menu_name=menu_name, price=price ,truemoney_number=truemoney_number)
    elif method == 'cash':
        return render_template('cash_confirm.html', username=username, menu_name=menu_name, price=price)
    elif method == 'bank':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT bank_account_number FROM payment_methods WHERE shop_name=?", (shop_name,))
        result = c.fetchone()
        conn.close()
        bank_account_number = result[0] if result else 'ไม่พบข้อมูลร้านค้า'
        return render_template('accountnum_confirm.html', username=username, menu_name=menu_name, price=price ,bank_account_number = bank_account_number)
    else:
        return "ไม่พบวิธีการชำระเงินนี้", 400








if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)
