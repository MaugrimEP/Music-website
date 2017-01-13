#! /usr/bin/env python3
from .app import app
from flask import render_template
from flask import url_for
from application import models

@app.route("/")
def home():
	return render_template(
	"home.html",
	title="Home",
	SizeSample=10,
	musics=models.getSimpleSample(10),
	)

@app.route("/musics/<int:id>")
def music_by_id(id):
	music=models.music_by_id(id)
	genres=models.genresFromMusicId(id)
	author=models.author_by_id(id)
	parent=models.author_by_id(id)
	return render_template(
	"music_by_id.html",
	music=music,
	genres=genres,
	author=author,
	parent=parent,
	)

@app.route("/authors/<int:id>")
def musics_by_author(id):
	author=models.author_by_id(id)
	return render_template(
	"musics_by_author.html",
	author=author,
	)

@app.route("/musics/<string:letter>")
def musics_all(letter='A'):
	tableau=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	listeMusics=models.musics_by_letter(letter)
	return render_template(
	"musics_all.html",
	letter=letter,
	listeMusics=listeMusics,
	tableau=tableau,
	)

@app.route("/authors/<string:letter>")
def authors_all(letter='A'):
	tableau=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	listeAuthors=models.authors_by_letter(letter)
	return render_template(
	"authors_all.html",
	letter=letter,
	listeAuthors=listeAuthors,
	tableau=tableau,
	)
