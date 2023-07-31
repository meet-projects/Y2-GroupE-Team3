from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
# app.config['SECRET_KEY'] = 'super-secret-key'



@app.route('/')
def about():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)