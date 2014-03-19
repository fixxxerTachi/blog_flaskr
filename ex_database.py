from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine=create_engine('mysql://username:password@localhost/prac_flask')
db_session=scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base=declarative_base()
Base.query=db_session.query_property()

def init_db():
	from models import User	
	Base.metadata.create_all(bind=engine)
