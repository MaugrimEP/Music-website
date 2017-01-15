#! /usr/bin/env python3
from .app import app, db
from flask import render_template
from flask import url_for, redirect
from application import models

from flask_login import logout_user

from flask_login import login_user, current_user
from flask import request

from flask_login import login_required

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
	# isBy=len([m for m in author.musics])!=0
	# isParent=len([c for c in author.childrens])!=0
	listeBy=[m for m in models.getMusicsFromAuthor(id)]
	listeParent=[c for c in models.getMusicsFromParent(id)]
	return render_template(
	"musics_by_author.html",
	author=author,
	listeBy=listeBy,
	listeParent=listeParent,
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
@login_required
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

@app.route("/login", methods=("GET","POST",))
def login():
	f = models.LoginForm()
	if not f.validate_on_submit():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		user = f.get_authenticated_user()
		if user:
			login_user(user)
			next = f.next.data or url_for("home")
			return redirect(next)
	return render_template(
	"login.html",
	form = f,
	)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))
