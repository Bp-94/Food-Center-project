from flask import Flask, render_template


app = Flask(__name__)


@app.route('/cash')
def cash_page():

    return render_template('cash.html')

if __name__ == '__main__':
    app.run(debug=True)
