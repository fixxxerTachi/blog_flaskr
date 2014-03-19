from sqlalchemy import Column,Integer,DateTime,Unicode,ForeignKey,Text,Table,String
from admin_database import Base
from sqlalchemy.orm import relationship
from flaskext.bcrypt import Bcrypt
class Product(Base):
	__tablename__='products_products'
	id=Column(Integer,primary_key=True)
	code=Column(Unicode(100))
	brand_id=Column(Integer,ForeignKey('products_brand.id'))
	color_id=Column(Integer,ForeignKey('products_color.id'))
	price=Column(Integer)
	type_id=Column(Integer,ForeignKey('products_type.id'))
	quantity=Column(Integer)
	img=Column(Unicode(255))
	created=Column(DateTime)
	modified=Column(DateTime)
	brand=relationship('Brand')
	color=relationship('Color')
	type=relationship('Type')
	orders=relationship('Association')

	def __repr__(self):
		return "<Products:%s>" % self.code

class Brand(Base):
	__tablename__='products_brand'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(255))
	code=Column(Unicode(10))
	descripiton=Column(Text)
	img=Column(Unicode(255))
	target_id=Column(Integer,ForeignKey('products_target.id'))
	sex_id=Column(Integer,ForeignKey('products_sex.id'))
	sex=relationship('Sex')

	def __init__(self,name):
		self.name=name

	def __repr__(self):
		return self.name

	@classmethod
	def show_list(cls):
		brands=cls.query.all()
		return [(v.id,v.name) for v in brands]

class Sex(Base):
	__tablename__='products_sex'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(255))
	def __init__(self,name):
		self.name=name
	def __repr__(self):
		return self.name

class Target(Base):
	__tablename__='products_target'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(255))
	def __init__(self,name):
		self.name=name
	def __repr__(self):
		return self.name
		
class Color(Base):
	__tablename__='products_color'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(100))
	code=Column(Unicode(100))
	icon=Column(Unicode(100))
	def __init__(self,name):
		self.name=name
	def __repr__(self):
		return self.name
	@classmethod
	def show_list(cls):
		colors=cls.query.all()
		return [(v.id,v.name) for v in colors]

class Type(Base):
	__tablename__='products_type'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(100))
	def __init__(self,name):
		self.name=name
	def __repr__(self):
		return self.name
	
	@classmethod
	def show_list(cls):
		types=cls.query.all()
		return [(v.id,v.name) for v in types]
		
'''
association_table=Table('order_product',Base.metadata,
	Column('order_id',Integer,ForeignKey('orders.id')),
	Column('product_id',Integer,ForeignKey('products_products.id')),
	Column('created_at',DateTime),
	Column('updated_at',DateTime),
	Column('is_leveled',DateTime,nullable=False),
	Column('enkinlens_id',Integer),
	Column('leveledlens_id',Integer),
	Column('nolens_id',Integer),
	Column('status_id',Integer,nullable=False)
)
'''
class Association(Base):
	__tablename__='order_product'
	id=Column(Integer,primary_key=True)
	order_id=Column(Integer,ForeignKey('orders.id'))
	product_id=Column(Integer,ForeignKey('products_products.id'))
	created_at=Column(DateTime)
	updated_at=Column(DateTime)
	is_leveled=Column(Integer)
	enkinlens_id=Column(Integer,ForeignKey('products_enkinlens.id'))
	leveledlens_id=Column(Integer,ForeignKey('products_leveledlens.id'))
	nolens_id=Column(Integer,ForeignKey('products_nolens.id'))
	status_id=Column(Integer,ForeignKey('statuses.id'))
	product=relationship('Product')
	status=relationship('Status')
	leveledlens=relationship('LeveledLens')
	enkinlens=relationship('EnkinLens')
	nolens=relationship('NoLens')

class Order(Base):
	__tablename__='orders'
	id=Column(Integer,primary_key=True)
	user_id=Column(Integer,ForeignKey('users.id'))
	address_id=Column(Integer,ForeignKey('addresses.id'))
	no_member_id=Column(Integer,ForeignKey('no_members.id'))
	created_at=Column(DateTime)
	updated_at=Column(DateTime)
	payment=Column(Unicode(100))
	total_price=Column(Integer)
	products=relationship('Association')

class EnkinLens(Base):
	__tablename__='products_enkinlens'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(200))
	def __init__(self,name):
		self.name=name
	def __repr__(self):
		return self.name

class LeveledLens(Base):
	__tablename__='products_leveledlens'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(255))
	def __init__(self,name):
		self.name=name
	def __repr__(self):
		return self.name

class NoLens(Base):
	__tablename__='products_nolens'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(255))
	def __init__(self,name):
		self.name=name
	def __repr__(self):
		return self.name

class Status(Base):
	__tablename__='statuses'
	id=Column(Integer,primary_key=True)
	status=Column(Unicode(10))
	def __init__(self,name):
		self.status=name
	def __repr__(self):
		return self.status
		

class User(Base):
	__tablename__='users'
	id=Column(Integer,primary_key=True)
	name=Column(Unicode(255))
	email=Column(Unicode(255))

class Address(Base):
	__tablename__='addresses'
	id=Column(Integer,primary_key=True)

class NoMember(Base):
	__tablename__='no_members'
	id=Column(Integer,primary_key=True)

class Admin(Base):
	__tablename__='admins'
	id=Column(Integer,primary_key=True)
	username=Column(Unicode(100))
	password=Column(Unicode(255))
	def __init__(self,username,password):
		self.username=username
		self.password=password
	def __reper__(self):
		return "<Admin %s:%s>" % (self.username,self.password)

