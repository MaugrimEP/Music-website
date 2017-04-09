# INSTALLATION
```
$ virtualenv -p python3 venv

$ source venv/bin/activate

$ cd rock-web/

$ pip install -r requirements.txt
===

$ pip install Flask
$ pip install Flask_script
$ pip install Flask_bootstrap
$ pip install Flask_sqlalchemy
$ pip install Flask_login
$ pip install Flask_json
$ pip install Flask_wtf
$ pip install pyyaml
===
$ ./manage.py loaddb albums.yml
```

# Launch server

```
$ ./manage.py runserver
http://localhost:5000/
http://localhost:5000/musicDetails/29367
```
