from tachilab_database import db
import datetime

class Article(db.Model):
	__tablename__='articles'
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.Unicode(255))
	contents=db.Column(db.Text)
	category_id=db.Column(db.Integer,db.ForeignKey('categories.id'))
	created_at=db.Column(db.DateTime)
	updated_at=db.Column(db.DateTime)
	tag=db.Column(db.Unicode(100))
	category=db.relationship('Category')
	def __init__(self,title,contents,category,tag):
		self.title=title
		self.contents=contents
		self.category=category
		self.tag=tag
		self.created_at=datetime.datetime.now()
		self.updated_at=datetime.datetime.now()

	def __repr__(self):
		return '<Artilce %r>' % self.title

class Category(db.Model):
	__tablename__='categories'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.Unicode(255))
	created_at=db.Column(db.DateTime)
	updated_at=db.Column(db.DateTime)
	def __init__(self,name):
		self.name=name
		self.updated_at=datetime.datetime.now()
		self.created_at=datetime.datetime.now()
	
	def __repr__(self):
		return '<Category %r>' % self.name
	
	@classmethod
	def show_list(cls):
		lists=cls.query.all()
		return [(c.id,c.name) for c in lists]

class User(db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.Unicode(255))
	password=db.Column(db.Unicode(255))
	created_at=db.Column(db.DateTime)
	updated_at=db.Column(db.DateTime)

	def __init__(self,username,password):
		self.username=username
		self.password=password

	def __repr__(self):
		return self.username
