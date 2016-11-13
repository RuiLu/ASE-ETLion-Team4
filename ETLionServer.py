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

from flask_socketio import SocketIO, disconnect, emit

from forms import SignupForm, LoginForm

from models import db, User
from Enum import POST, GET
from Enum import ORDER_DISCOUNT, ORDER_SIZE, INVENTORY, TRADING_FREQUENCY, QUERY_URL, ORDER_URL
from ETLionCore import ETLionCore
from AppUtil import init_app


app = init_app()

db.init_app(app)

async_mode = "threading"
socketio = SocketIO(app, async_mode=async_mode)
thread = None

@socketio.on('connect')
def test_connect():
    print "Connected with Socket-IO !!!!!!!!!!!!!!!!!!!!!!!"

@socketio.on('calculate')
def calculate(post_params):
    print post_params

    order_discount = int(post_params[ORDER_DISCOUNT])
    order_size = int(post_params[ORDER_SIZE])
    inventory = int(post_params[INVENTORY])
    trading_freq = int(post_params[TRADING_FREQUENCY])

    # Start with all shares and no profit
    total_qty = qty = inventory
    pnl = 0

    # Repeat the strategy until we run out of shares.
    while qty > 0:
        # Query the price once every N seconds.
        time.sleep(trading_freq)

        quote = json.loads(urllib2.urlopen(QUERY_URL.format(random.random())).read())
        price = float(quote['top_bid']['price'])
         
        # Attempt to execute a sell order.
        discount_price = price - order_discount
        order_args = (order_size, discount_price)
        print "Executing 'sell' of {:,} @ {:,}".format(*order_args)
        url   = ORDER_URL.format(random.random(), *order_args)
        order = json.loads(urllib2.urlopen(url).read())

        # Update the PnL if the order was filled.
        if order['avg_price'] > 0:
            price    = order['avg_price']
            notional = price * order_size
            pnl += notional
            qty -= order_size
            print "Sold {:,} for ${:,}/share, ${:,} notional".format(order_size, price, notional)
            print "PnL ${:,}, Qty {:,}".format(pnl, qty)
            emit('trade_log',
                {
                    'order_size': order_size,
                    'discount_price': discount_price,
                    'share_price': price,
                    'notional': notional,
                    'pnl': pnl,
                    'total_qty': total_qty
                }
            )
        else:
            print "Unfilled order; $%s total, %s qty" % (pnl, qty)

        time.sleep(1)

def is_user_in_session():
    return ('email' in session and 'username' in session)

@app.route('/')
@app.route('/index')
def index():
    if is_user_in_session():
        return redirect(url_for('trade', username=session['username']))
    else:
        return render_template("index.html", async_mode=socketio.async_mode)

@app.route('/trade')
def trade():
    if is_user_in_session():
        return render_template("trade.html", async_mode=socketio.async_mode, username=session['username'])
    else:
        return redirect(url_for('index', username=session['username']))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if is_user_in_session():
        return redirect(url_for('trade', username=session['username']))

    form = SignupForm(request.form)

    if request.method == "POST":
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            session['username'] = newuser.firstname + ' ' + newuser.lastname
            return redirect(url_for('index', username=session['username']))
    elif request.method == "GET":
        return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if is_user_in_session():
        return redirect(url_for('trade', username=session['username']))

    form = LoginForm(request.form)

    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            session['email'] = user.email
            session['username'] = user.firstname + ' ' + user.lastname
            return redirect(url_for('index', username=session['username']))
        else:
            return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('username', None)
    return redirect('/')

if __name__ == "__main__":
    import click

    @click.command()
    @click.argument('HOST', default='127.0.0.1')
    @click.argument('PORT', default=4156, type=int)
    def socketio_app_run(host, port):
        try:
            HOST, PORT = host, port
            print "ET Lion Server Running On %s:%d" % (HOST, PORT)
            socketio.run(app, host=HOST, port=PORT, debug=True)
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            socketio.stop()

    socketio_app_run()
