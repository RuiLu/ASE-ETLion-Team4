import urllib2
import time
import json
import random

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

from Enum import POST, GET
from Enum import ORDER_DISCOUNT, ORDER_SIZE, INVENTORY, TRADING_FREQUENCY
from ETLionCore import ETLionCore

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

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
