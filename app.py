from flask import Flask, render_template


app = Flask(__name__)


@app.route('/truewallet')
def truewallet_page():

    return render_template('truewallet.html')

if __name__ == '__main__':
    app.run(debug=True)
