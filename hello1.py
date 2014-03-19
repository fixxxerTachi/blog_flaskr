from flask import Flask,url_for,render_template,abort
app=Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello Falsk!'

@app.route('/css/')
def test_static():
	return url_for('static',filename='style.css')

@app.route('/template/')
@app.route('/template/<name>')
def test_template(name=None):
	app.logger.debug('a value for debugging')
	return render_template('hello.html',name=name)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404

if __name__=='__main__':
	app.debug=True
	app.run()

