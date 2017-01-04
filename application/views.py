#! /usr/bin/env python3
from .app import app

@app.route("/")
def home():
	return "<h1>Hello World</h1>"