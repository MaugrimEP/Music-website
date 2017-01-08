#! /usr/bin/env python3
from .app import app
from flask import render_template, url_for
from application import models

@app.route("/")
def home():
	return render_template(
	"home.html",
	title="Home",
	SizeSample=10,
	musics=models.getSimpleSample(10),
	)
