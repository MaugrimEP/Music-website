from .app import db

class Author(db.Model):
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
        return "<Music (%d) %s" % (self.id,self.title)
