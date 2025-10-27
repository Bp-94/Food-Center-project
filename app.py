from flask import Flask ,render_template
app = Flask(__name__)

if __name__ == "__main__":
    app.run()
@app.route('/')
def menu():
    return render_template("main_menu.html")