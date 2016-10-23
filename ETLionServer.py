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
from flask_socketio import SocketIO, disconnect

from forms import SignupForm, LoginForm

from models import db, User
from Enum import POST, GET
from Enum import ORDER_DISCOUNT, ORDER_SIZE, INVENTORY, TRADING_FREQUENCY
from ETLionCore import ETLionCore
from AppUtil import init_app

app = init_app()

db.init_app(app)

async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

@socketio.on('connect')
def test_connect():
    print "Connected!!!!!!!!!!!!!!!!!!!!!!!"

@socketio.on('my_event')
def test_message(message):
    print message

@socketio.on('calculate')
def calculate(post_params):
    print post_params
    params = {
        ORDER_DISCOUNT: int(post_params[ORDER_DISCOUNT]), 
        ORDER_SIZE: int(post_params[ORDER_SIZE]), 
        INVENTORY: int(post_params[INVENTORY]), 
        TRADING_FREQUENCY: int(post_params[TRADING_FREQUENCY])
    }
    et_lion_core = ETLionCore(**params)
    et_lion_core.trade()
    
@app.route('/')
def index():
    return render_template("index.html", async_mode=socketio.async_mode)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if 'email' in session:
        return redirect('/')

    form = SignupForm()

    if request.method == "POST":
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect('/')

    elif request.method == "GET":
        return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect('/')

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
                return redirect('/')
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect('/')


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=4156, type=int)
    def socketio_app_run(debug, host, port):
        HOST, PORT = host, port
        print "ET Lion Server Running On %s:%d" % (HOST, PORT)
        socketio.run(app, host=HOST, port=PORT, debug=debug)

    socketio_app_run()
