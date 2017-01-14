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
    return Music.query.filter(*opFilter).all()

def authors_by_letter(letter):
    opFilter=[Author.name.like(letter.lower()+"%")|(Author.name.like(letter.upper()+"%"))]
    return Author.query.filter(*opFilter).all()

def musics_Autre():
    T=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    t=T+[l.lower() for l in T]
    opFilter=[~(Music.title.like(letter+"%")) for letter in t]
    return Music.query.filter(*opFilter)

def authors_Autre():
    T=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    t=T+[l.lower() for l in T]
    opFilter=[~(Author.name.like(letter+"%")) for letter in t]
    return Author.query.filter(*opFilter)
