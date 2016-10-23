from flask import Flask

def init_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xtifhtrqnydawd:n3xiwg41_vMzqBKG99pKt3gX4D@ec2-50-19-219-148.compute-1.amazonaws.com:5432/d9265ge1sbuard'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = "development-key"
    return app

