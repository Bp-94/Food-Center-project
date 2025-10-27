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