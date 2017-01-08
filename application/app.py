#! /usr/bin/env python3
import os.path
from flask import Flask
app = Flask(__name__)
app.debug = True

from flask_script import Manager
manager = Manager(app)

app.config['BOOTSTRAP_SERVER_LOCAL']=True

from flask_bootstrap import Bootstrap
Bootstrap(app)

def mkpath(p):
    return os.path.join(os.path.dirname(__file__),p)

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI']=('sqlite:///'+mkpath('../albums.db'))
db=SQLAlchemy(app)
