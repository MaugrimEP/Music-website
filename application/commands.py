from .app import manager,db

@manager.command
def loaddb(filename):

    #create the tables from models.py
    db.create_all()

    #data loading
    import yaml
    musics = yaml.load(open(filename))

    #models loading
    from .models import Author, Genre, Classification, Music

    #authors creation
    calculetedAuthors={}
    calculetedGenres={}
    calculetedMusics={}
    calculetedClassification=set()
    for music in musics:
        author=music["by"]
        if author not in calculetedAuthors:
            o=Author(name=author)
            db.session.add(o)
            calculetedAuthors[author]=o

        author=music["parent"]
        if author not in calculetedAuthors:
            o=Author(name=author)
            db.session.add(o)
            calculetedAuthors[author]=o
    db.session.commit()


        #Genres creation
    for music in musics:
        lesGenres=music["genre"]
        for genre in lesGenres:
            if genre not in calculetedGenres:
                o=Genre(genre=genre)
                db.session.add(o)
                calculetedGenres[genre]=o
    db.session.commit()

    #Musics creation
    #if fact we dont care about the id given into the yaml file because its safer to recalcute the ids.
    #in case an id is missing into the yaml file
    for music in musics:
        if music["title"] not in calculetedMusics and len(music["title"])!=0:
            by = calculetedAuthors[music["by"]]
            parent = calculetedAuthors[music["parent"]]
            o = Music(
                    by = by.id,
                    img = music["img"],
                    parent = parent.id,
                    releaseYear = music["releaseYear"],
                    title = music["title"],
            )
            db.session.add(o)
            calculetedMusics[music["title"]]=o
    db.session.commit()


    #Classification creation
    for music in musics:
        if len(music["title"])!=0:
            genres=music["genre"]
            for genre in genres:
                idGenre = calculetedGenres[genre].id
                idMusic = calculetedMusics[music["title"]].id

                if (idGenre,idMusic) not in calculetedClassification:
                    o=Classification(
                        idGenre=idGenre,
                        idMusic=idMusic,
                    )
                    calculetedClassification.add((idGenre,idMusic))
                    db.session.add(o)
    db.session.commit()


@manager.command
def syncdb():
    '''creates the missing tables'''
    db.create_all()
