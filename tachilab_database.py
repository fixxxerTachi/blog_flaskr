from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
import datetime

app=Flask(__name__)
cache=Cache(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://tachi:tachi@localhost/puppetz_blog'
db=SQLAlchemy(app)

def init_db():
	import tachilab_models
	db.create_all()
