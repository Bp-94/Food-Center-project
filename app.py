from flask import Flask, render_template


app = Flask(__name__)


@app.route('/payment')
def payment_page():

    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
