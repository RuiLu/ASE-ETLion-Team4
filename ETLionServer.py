import urllib2
import time
import json
import random

from flask import Flask
from flask import request
from flask import render_template


from Enum import POST, GET
from ETLionCore import ETLionCore

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/calculate', methods=[POST, GET])
def calculate():
    et_lion_core = ETLionCore(request.form)
    et_lion_core.trade()
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
