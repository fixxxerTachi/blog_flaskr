from flask import Flask,render_template,g
app=Flask(__name__)
from database import db_session
from models import User

@app.route('/')
def index():
	users=db_session.query(User).all()
	return render_template('show_users.html',users=users)

if __name__=='__main__':
	app.debug=True
	app.run()
