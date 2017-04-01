#! /usr/bin/env python3
from .app import app, db
from flask import Flask, render_template, url_for, redirect, request, jsonify
from application import models

from flask_login import logout_user, login_user, current_user, login_required
from flask_json import FlaskJSON, JsonError, json_response, as_json

import math

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
	listeBy=[m for m in models.getMusicsFromAuthor(id)]
	listeParent=[c for c in models.getMusicsFromParent(id)]
	return render_template(
	"musics_by_author.html",
	author=author,
	listeBy=listeBy,
	listeParent=listeParent,
	)

@app.route("/musics/<string:params>")
def musics_all(params='A1'):
	letter=params[0]
	page=int(params[1:])-1
	sizeSample=20

	listeMusics=models.musics_by_letter(letter)
	fin=min(len(listeMusics),page+sizeSample)
	sample=[listeMusics[i] for i in range(page,fin)]
	nbPage=math.ceil(len(listeMusics)/sizeSample)

	return render_template(
	"musics_all.html",
	letter=letter,
	listeMusics=sample,
	tableau=tableau,
	page=page+1,
	nbPage=nbPage+1,
	listePages=[i for i in range(1,nbPage+1)]
	)

@app.route("/musics/Autre/<int:page>")
def musics_autre(page=1):
	page=page-1
	sizeSample=20

	listeMusics=models.musics_Autre()
	fin=min(len(listeMusics),page+sizeSample)
	sample=[listeMusics[i] for i in range(page,fin)]
	nbPage=math.ceil(len(listeMusics)/sizeSample)

	return render_template(
	"musics_autre.html",
	listeMusics=sample,
	tableau=tableau,
	page=page+1,
	nbPage=nbPage+1,
	listePages=[i for i in range(1,nbPage+1)],
	)

@app.route("/authors/<string:params>")
def authors_all(params='A1'):

	letter=params[0]
	page=int(params[1:])-1
	sizeSample=20

	listeAuthors=models.authors_by_letter(letter)

	fin=min(len(listeAuthors),page+sizeSample)
	sample=[listeAuthors[i] for i in range(page,fin)]
	nbPage=math.ceil(len(listeAuthors)/sizeSample)

	return render_template(
	"authors_all.html",
	letter=letter,
	listeAuthors=sample,
	tableau=tableau,
	page=page+1,
	nbPage=nbPage+1,
	listePages=[i for i in range(1,nbPage+1)]
	)

@app.route("/authors/Autre/<int:page>")
def authors_autre(page=1):

	page=page-1
	sizeSample=20

	listeAuthors=models.authors_Autre()

	fin=min(len(listeAuthors),page+sizeSample)
	sample=[listeAuthors[i] for i in range(page,fin)]
	nbPage=math.ceil(len(listeAuthors)/sizeSample)

	return render_template(
	"authors_autre.html",
	listeAuthors=sample,
	tableau=tableau,
	page=page+1,
	nbPage=nbPage+1,
	listePages=[i for i in range(1,nbPage+1)],
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

@app.route("/r/author")
def authorR():
	form = models.AuthorRForm()
	return render_template(
	"authorR.html",
	form=form,
	)

@app.route("/redirect/authorR",  methods=("POST",))
def author_search():
	form = models.AuthorForm()
	#if form.validate_on_submit():
	return redirect(url_for('displayAR',name=form.name.data))
	return render_template(
	"authorR.html",
	form = form,
	)

@app.route("/display/authorR/<string:name>")
def displayAR(name):
	listeAuthors = models.getAuthorsFromNames(name)
	return render_template(
	"displayAR.html",
	listeAuthors=listeAuthors,
	name=name,
	)

@app.route("/saveCommentaire",methods=['POST'])
@login_required
def saveCommentaire():
	commentaire = request.get_json(force=True)
	idFilm = commentaire["musicId"]
	username = commentaire["username"]
	texte = commentaire["texte"]
	dbCommentaire = models.Commentaire(idFilm=idFilm,username=username,texte=texte)
	db.session.add(dbCommentaire)
	db.session.commit()
	return jsonify(commentaire)

@app.route("/getListCommentaires", methods=['GET','POST'])
def getListCommentaires():
	idMusic = request.args.get("idMusic")
	commentaires = models.getCommentairesFromIdMusic(idMusic)
	return jsonify(commentaires)

@app.route("/supprimerCommentaire", methods=['GET','POST'])
@login_required
def supprimerCommentaire():
	ressource = request.get_json(force=True)
	idCom = ressource["id"]
	DBCom = models.getCommentaireById(idCom)
	db.session.delete(DBCom)
	db.session.commit()
	return jsonify(idCom)

@app.route("/editerCommentaire", methods=['GET','POST'])
def editierCommentaire():
	ressource = request.get_json(force=True);
	idCom = ressource["id"]
	newText = ressource["text"]
	dbCommentaire = models.getCommentaireById(idCom)
	dbCommentaire.texte=newText
	db.session.commit()
	return jsonify(ressource)
