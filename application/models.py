from .app import db

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

from flask_login import UserMixin
from wtforms import PasswordField
from wtforms.validators import Length, EqualTo

from hashlib import sha256

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(64))

    def get_id(self):
        return self.id

class RegistrationForm(FlaskForm):
    id = HiddenField('id')
    username = StringField('UserName', validators= [DataRequired(),Length(min=4, max=25)])
    password = PasswordField('New Password', validators= [ DataRequired(), EqualTo('confirm', message='Passwords must match') ] )
    confirm = PasswordField ('Repeat Password')

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])

class Author(db.Model):

    @staticmethod
    def getName(author):
        return author.name

    @staticmethod
    def trie(listeAuthors):
        return sorted(listeAuthors,key=Author.getName)

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))

    def __repr__(self):
        return "<Author (%d) %s>"%(self.id,self.name)


class Genre(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    genre=db.Column(db.String(200))

    def __repr__(self):
        return "<Genre (%d) %s>"(self.id,self.genre)

class Classification(db.Model):
    idGenre=db.Column(db.Integer,db.ForeignKey("genre.id"),primary_key=True)
    idMusic=db.Column(db.Integer,db.ForeignKey("music.id"),primary_key=True)

    #now the backref to get all the genres for one music
    genre = db.relationship("Music",
        backref=db.backref("genres",lazy="dynamic"))


class Music(db.Model):

    @staticmethod
    def getTitle(music):
        return music.title

    @staticmethod
    def trie(listeMusics):
        return sorted(listeMusics,key=Music.getTitle)

    by=db.Column(db.Integer,db.ForeignKey("author.id"))
    #we also want to have the musics for one author
    author = db.relationship("Author",
        backref=db.backref("musics",lazy="dynamic"))


    id=db.Column(db.Integer,primary_key=True)
    # we dont put the genre here but in a new talbe
    img=db.Column(db.String(200))
    parent=db.Column(db.String(200))
    releaseYear=db.Column(db.Integer)
    title=db.Column(db.String(200))

    def __repr__(self):
        return "<Music (%d) %s>" % (self.id,self.title)

def getSimpleSample(SizeSample):
    return Music.query.limit(SizeSample).all()

def music_by_id(id):
    return Music.query.get_or_404(id)

def genresFromMusicId(id):
    return Genre.query.join(Classification).filter(Classification.idMusic==id).all()

def author_by_id(id):
    return Author.query.get_or_404(id)

def musics_by_letter(letter):
    opFilter=[Music.title.like(letter.lower()+"%")|(Music.title.like(letter.upper()+"%"))]
    return Music.trie(Music.query.filter(*opFilter).all())

def authors_by_letter(letter):
    opFilter=[Author.name.like(letter.lower()+"%")|(Author.name.like(letter.upper()+"%"))]
    return Author.trie(Author.query.filter(*opFilter).all())

def musics_Autre():
    T=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    t=T+[l.lower() for l in T]
    opFilter=[~(Music.title.like(letter+"%")) for letter in t]
    return Music.trie(Music.query.filter(*opFilter))

def authors_Autre():
    T=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    t=T+[l.lower() for l in T]
    opFilter=[~(Author.name.like(letter+"%")) for letter in t]
    return Author.trie(Author.query.filter(*opFilter))

def add_User(username, password):
    m = sha256()
    m.update(password.encode())
    u = User(username=username, password=m.hexdigest())
    db.session.add(u)
    db.session.commit()
