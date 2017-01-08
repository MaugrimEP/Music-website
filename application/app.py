#! /usr/bin/env python3
from flask import Flask
import os.path

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),p))

app = Flask(__name__)
app.debug= True

from flask.ext.script import Manager
manager = Manager(app)

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMYD_DATABASE_URI']=('sqlite:///'+mkpath('../myapp.db'))
db=SQLAlchemy(app)
