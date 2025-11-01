from flask import Flask, render_template


app = Flask(__name__)


@app.route('/accountnum')
def accountnum_page():

    return render_template('accountnum.html')

if __name__ == '__main__':
    app.run(debug=True)
