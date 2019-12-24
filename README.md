# Flask-RestAPI SWAGGER

#### Running Flask
```
pipenv shell
export FLASK_APP=run.py
export FLASK_ENV=development
rm -rf * migrations app/db.sqlite 
flask db init 
flask db migrate --message 'user'
flask db upgrade
python test.py
```
