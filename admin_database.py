from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
engine=create_engine('mysql+mysqldb://username:password@localhost/online_store?charset=utf8',convert_unicode=True,echo=True)
db_session=scoped_session(sessionmaker(bind=engine))
Base=declarative_base()
Base.query=db_session.query_property()

def init_db():
	import admin_models
	Base.metadata.create_all(engine)


