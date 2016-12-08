import json
import random
import urllib2

from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for

from flask_socketio import SocketIO

from forms import SignupForm, LoginForm, saveOrderForm, saveTradeForm

from models import db, User, Order, Trade
from Enum import POST, GET
from Enum import QUERY_URL, ORDER_URL
from AppUtil import init_app

app = init_app()

db.init_app(app)

socketio = SocketIO(app, async_mode=None)
thread = None
is_order_canceled = False

def background_thread_place_order(
        order_discount, order_size, inventory, trading_frequency,
    ):
    order_discount = int(order_discount)
    order_size = int(order_size)
    inventory = int(inventory)
    trading_freq = int(trading_frequency)

    # Start with all shares and no profit
    total_qty = qty = inventory
    pnl = 0
    # Repeat the strategy until we run out of shares.
    while qty > 0:
        global is_order_canceled
        if is_order_canceled:
            is_order_canceled = False
            break
        # Query the price once every N seconds.
        socketio.sleep(trading_freq)
        quote = json.loads(
            urllib2.urlopen(QUERY_URL.format(random.random())).read()
        )
        price = float(quote['top_bid']['price'])
        # Attempt to execute a sell order.
        discount_price = price - order_discount
        order_args = (order_size, discount_price)
        print "Executing 'sell' of {:,} @ {:,}".format(*order_args)
        url   = ORDER_URL.format(random.random(), *order_args)
        order = json.loads(urllib2.urlopen(url).read())

        # Update the PnL if the order was filled.
        if order['avg_price'] <= 0:
            print "Unfilled order; $%s total, %s qty" % (pnl, qty)
        else:
            price    = order['avg_price']
            notional = int(price * order_size)
            pnl += notional
            qty -= order_size
            print "Sold {:,} for ${:,}/share, ${:,} notional".format(
                order_size, price, notional
            )
            emit_params = {
                'order_size': order_size,
                'discount_price': discount_price,
                'share_price': price,
                'notional': notional,
                'pnl': pnl,
                'total_qty': total_qty
            }
            print "PnL ${:,}, Qty {:,}".format(pnl, qty)
            socketio.emit('trade_log', emit_params)

def exec_cancel_order():
    global is_order_canceled
    is_order_canceled = True

def exec_resume_order():
    global is_order_canceled
    is_order_canceled = False

@socketio.on('connect')
def test_connect():
    print "Connected with Socket-IO !!!!!!!!!!!!!!!!!!!!!!!"

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

@socketio.on('calculate')
def calculate(post_params):
    print post_params
    if post_params.get("is_for_test"):
        del post_params["is_for_test"]
        background_thread_place_order(**post_params)
    else:
        global thread
        thread = socketio.start_background_task(
            target=background_thread_place_order, **post_params
        )

def is_user_in_session():
    return ('email' in session and 'username' in session)

@app.route('/')
@app.route('/index')
def index():
    form = LoginForm(request.form)
    if is_user_in_session():
        return redirect(url_for('trade', username=session['username']))
    else:
        return render_template("index.html", async_mode=socketio.async_mode, form=form)

@socketio.on('cancel_order')
def cancel(post_params={}):
    exec_cancel_order()
    if post_params and post_params.get('is_for_test'):
        emit_params = {"is_order_canceled": is_order_canceled}
        socketio.emit('cancel_order', emit_params)

@app.route('/trade')
def trade():
    if not is_user_in_session():
        return redirect(url_for('index', username=session['username']))
    else:
        return render_template(
            "trade.html",
            async_mode=socketio.async_mode,
            username=session['username']
        )

@app.route("/signup", methods=[GET, POST])
def signup():
    exec_resume_order()

    if is_user_in_session():
        return redirect(url_for('trade', username=session['username']))

    form = SignupForm(request.form)

    if request.method == POST:
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            newuser = User(
                form.firstname.data, 
                form.lastname.data, 
                form.email.data, 
                form.password.data
            )
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            session['username'] = newuser.firstname + ' ' + newuser.lastname
            return redirect(url_for('index', username=session['username']))

    elif request.method == GET:
        return render_template('signup.html', form=form)

# To-DO
@app.route("/save_order", methods=[GET, POST])
def save_order():

    orderForm = saveOrderForm(request.form)
    traderForm = saveTradeForm(request.form)

    if request.method == POST:
        newOrder = Order(
            orderForm.type.data,
            orderForm.size.data,
            orderForm.inventory.data
        )
        db.session.add(newOrder)
        db.session.commit()

# @app.route("/login", methods=[GET, POST])
# def login():
#     if is_user_in_session():
#         return redirect(url_for('trade', username=session['username']))

#     form = LoginForm(request.form)

#     if request.method == POST:
#         email = form.email.data
#         password = form.password.data
#         user = User.query.filter_by(email=email).first()
#         if user is not None and user.check_password(password):
#             session['email'] = user.email
#             session['username'] = user.firstname + ' ' + user.lastname
#             return redirect(url_for('index', username=session['username']))
#         else:
#             return redirect(url_for('login'))

#     elif request.method == 'GET':
#         return render_template('login.html', form=form)

@app.route("/login", methods=[GET, POST])
def login():
    exec_resume_order()

    if is_user_in_session():
        return redirect(url_for('trade', username=session['username']))

    form = LoginForm(request.form)

    if request.method == POST:
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            session['email'] = user.email
            session['username'] = user.firstname + ' ' + user.lastname
            return redirect(url_for('trade', username=session['username']))
        else:
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('index.html', form=form)

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('username', None)
    exec_cancel_order()
    return redirect('/')

if __name__ == "__main__":
    import click

    @click.command()
    @click.argument('HOST', default='127.0.0.1')
    @click.argument('PORT', default=6111, type=int)
    def socketio_app_run(host, port):
        try:
            HOST, PORT = host, port
            print "ET Lion Server Running On %s:%d" % (HOST, PORT)
            socketio.run(app, host=HOST, port=PORT, debug=True)
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            socketio.stop()

    socketio_app_run()
