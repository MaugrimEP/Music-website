#! /usr/bin/env python3
from .app import app, db
from flask import render_template
from flask import url_for, redirect
from application import models

tableau=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

@app.route("/")
def home():
	return render_template(
	"home.html",
	title="Home",
	SizeSample=10,
	musics=models.getSimpleSample(10),
	)

@app.route("/musicDetails/<int:id>")
def music_by_id(id):
	music=models.music_by_id(id)
	genres=models.genresFromMusicId(id)
	author=models.author_by_id(music.by)
	parent=models.author_by_id(music.parent)
	return render_template(
	"music_by_id.html",
	music=music,
	genres=genres,
	author=author,
	parent=parent,
	)

@app.route("/authorDetails/<int:id>")
def musics_by_author(id):
	author=models.author_by_id(id)
	return render_template(
	"musics_by_author.html",
	author=author,
	)

@app.route("/musics/<string:letter>")
def musics_all(letter='A'):
	listeMusics=models.musics_by_letter(letter)
	return render_template(
	"musics_all.html",
	letter=letter,
	listeMusics=listeMusics,
	tableau=tableau,
	)

@app.route("/musics/Autre")
def musics_autre():
	listeMusics=models.musics_Autre()
	return render_template(
	"musics_autre.html",
	listeMusics=listeMusics,
	tableau=tableau,
	)

@app.route("/authors/<string:letter>")
def authors_all(letter='A'):
	listeAuthors=models.authors_by_letter(letter)
	return render_template(
	"authors_all.html",
	letter=letter,
	listeAuthors=listeAuthors,
	tableau=tableau,
	)

@app.route("/authors/Autre")
def authors_autre():
	listeAuthors=models.authors_Autre()
	return render_template(
	"authors_autre.html",
	listeAuthors=listeAuthors,
	tableau=tableau,
	)

@app.route("/edit/author/<int:id>")
def edit_authors(id):
	a = models.author_by_id(id)
	f = models.AuthorForm(id=a.id, name=a.name)
	return render_template(
	"edit_authors.html",
	author=a,
	form=f,
	)

@app.route("/save/author/<int:id>", methods=("POST",))
def save_author(id):
	a = None
	f = models.AuthorForm()
	if f.validate_on_submit():
		id = int(f.id.data)
		a = models.author_by_id(id)
		a.name = f.name.data
		db.session.commit()
		return redirect(url_for("musics_by_author",id=a.id))
	return render_template(
	"edit_authors.html",
	author=models.author_by_id(id),
	form=f,
	)

@app.route("/add/author")
def add_authors():
	f = models.AuthorForm()
	return render_template(
	"add_authors.html",
	form=f,
	)

@app.route("/new/author", methods=("POST",))
def new_author():
	a = None
	f = models.AuthorForm()
	if f.validate_on_submit():
		a = models.Author(name=f.name.data)
		db.session.add(a)
		db.session.commit()
		return redirect(url_for('musics_by_author', id=a.id))
	return render_template(
	"add_authors.html",
	form=f,
	)

@app.route('/sign_up')
def sign_up():
	form = models.RegistrationForm()
	return render_template(
	"sign_up.html",
	form = form
	)

@app.route('/register', methods=['POST'])
def register():
	user = None
	form = models.RegistrationForm()
	if form.validate_on_submit():
		models.add_User(
				username=form.username.data,
				password=form.password.data,)
		return redirect(url_for('home'))
	return render_template(
		'sign_up.html',
		form=form
		)
