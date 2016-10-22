import urllib2
import time
import json
import random

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for
from forms import SignupForm, LoginForm

from models import db, User
from Enum import POST, GET
from Enum import ORDER_DISCOUNT, ORDER_SIZE, INVENTORY, TRADING_FREQUENCY
from ETLionCore import ETLionCore

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xtifhtrqnydawd:n3xiwg41_vMzqBKG99pKt3gX4D@ec2-50-19-219-148.compute-1.amazonaws.com:5432/d9265ge1sbuard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

app.secret_key = "development-key"

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if 'email' in session:
        return redirect(url_for(''))

    form = SignupForm()

    if request.method == "POST":
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for(''))

    elif request.method == "GET":
        return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect(url_for(''))

    form = LoginForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for(''))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/calculate', methods=[POST, GET])
def calculate():
    if request.method == POST:
        params = {
            ORDER_DISCOUNT: request.form[ORDER_DISCOUNT], 
            ORDER_SIZE: request.form[ORDER_SIZE], 
            INVENTORY: request.form[INVENTORY], 
            TRADING_FREQUENCY: request.form[TRADING_FREQUENCY]
        }
        et_lion_core = ETLionCore(**params)
        et_lion_core.trade()
        return redirect('/')
    else:
        print "get calculate"
        return redirect('/')

if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=4156, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:

            python server.py

        Show the help text using:

            python server.py --help

        """
        HOST, PORT = host, port
        print "ET Lion Server Running On %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
