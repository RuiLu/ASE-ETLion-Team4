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
from flask_socketio import SocketIO, send, emit, disconnect

from forms import SignupForm, LoginForm

from models import db, User
from Enum import POST, GET
from Enum import ORDER_DISCOUNT, ORDER_SIZE, INVENTORY, TRADING_FREQUENCY, QUERY_URL, ORDER_URL
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

    order_discount = int(post_params[ORDER_DISCOUNT])
    order_size = int(post_params[ORDER_SIZE])
    inventory = int(post_params[INVENTORY])
    trading_freq = int(post_params[TRADING_FREQUENCY])
    # et_lion_core = ETLionCore(**params)
    # et_lion_core.trade()

    # Start with all shares and no profit
    qty = inventory
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
            notional = float(price * order_size)
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
                    'qty': qty
                }
            )
        else:
            print "Unfilled order; $%s total, %s qty" % (pnl, qty)

        time.sleep(1)

    # while True :
    #     emit('trade_log',
    #         {
    #             'order_size': 1,
    #             'discount_price': 10,
    #             'share_price': 200,
    #             'notional': 11,
    #             'pnl': 11,
    #             'qty': 11
    #         }
    #     )
    #     time.sleep(5)
    
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
