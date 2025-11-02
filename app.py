from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask ,render_template
app = Flask(__name__)

@app.route('/')
def menu():
    return render_template("main_menu.html")

@app.route('/income')
def income():
    return render_template("income.html")

if __name__ == "__main__":
    app.run()
