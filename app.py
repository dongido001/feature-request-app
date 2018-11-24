from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'very secret, do you believe? Nah!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')
app.config['SECRETE_KEY'] = os.getenv('SECRETE_KEY') 

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Client, User, Request
import seed

import views as views


if __name__ == '__main__':
    app.run()
    # serve(app, host='0.0.0.0', port=5000)
    # app.run()
    pass