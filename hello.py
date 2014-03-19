from flask import Flask
from flask import render_template,g
app=Flask(__name__)
@app.route('/')
def hello_world():
	return 'Hello World'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello1(name=None):
	g.name=name
	return render_template('hello.html')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404

from flask import session,redirect,url_for,escape,request
@app.route('/loggedin/')
def index():
	if 'username' in session:
		return 'Logged in as %s' % escape(session['username'])
	return 'you are not logged in'

@app.route('/login/',methods=['GET','POST'])
def login():
	if request.method=='POST':
		session['username']=request.form['username']
		return redirect(url_for('index'))
	return '''
		<!doctype html><html><body>
		<form action='' method='post'>
			<p><input type='text' name='username'></p>
			<p><input type='submit' value='Login'>
		</form></body></html>
	'''
@app.route('/logout/')
def logout():
	session.pop('username',None)
	return redirect(url_for('index'))

if __name__=='__main__':
	app.debug=True
	app.secret_key='hogefoo'
	app.run()
