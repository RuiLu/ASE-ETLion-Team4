import os

from flask import Flask

def init_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xtifhtrqnydawd:n3xiwg41_vMzqBKG99pKt3gX4D@ec2-50-19-219-148.compute-1.amazonaws.com:5432/d9265ge1sbuard'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = "development-key"
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = "etliontrade@gmail.com"

    dirname = os.path.dirname(os.path.abspath(__file__))
    f = open(dirname + "/password.txt", "r")
    app.config['MAIL_PASSWORD'] = f.read()

    app.config['MAIL_DEFAULT_SENDER'] = "etliontrade@gmail.com"
    return app