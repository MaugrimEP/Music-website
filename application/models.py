from .app import db

class Author(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))

    def __repr__(self):
        return "<Author (%d) %s>"%(self.id,self.name)

class Genre(db.Model):
    id=db.Column(db.Integer)
    name=db.Column(db.String(200))

class Music(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
    parent=db.Column(db.String(200))
    releaseYear=db.Column(db.Integer)
    img=db.Column(db.String(200))
