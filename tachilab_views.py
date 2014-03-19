from tachilab_database import app,db,cache
from tachilab_models import Article,Category,User
from flask import render_template,request,g,redirect,url_for,session
from sqlalchemy import or_
from wtforms import Form,TextField,SelectField,TextAreaField,PasswordField
from flaskext.bcrypt import Bcrypt
@app.before_request
def show_category():
	g.categories=Category.query.all()
	'''tag'''
	articles=Article.query.all()
	arr=[]
	for a in articles:
		if a.tag:
			arr.extend(a.tag.split(','))
	g.arr=set(arr)
	authenticated=['/add_article/','/edit_article/']
	if request.path in authenticated:
		user=session.get('user',None)
		if not user:
			return redirect('/login/')


@app.route('/')
@cache.cached(timeout=50)
def show_article():
	page=request.args.get('page',1)
	category=request.args.get('category','')	
	keyword=request.args.get('keyword','')
	tag=request.args.get('tag','')
	if category:
		articles=Article.query.filter_by(category_id=category).order_by('id desc').paginate(page,3)
	elif keyword:
		articles=Article.query.filter(
			or_(Article.title.like('%' + keyword + '%'),Article.contents.like('%' + keyword + '%'))) \
				.order_by('id desc').paginate(page,3)
	elif tag:
		articles=Article.query.filter(Article.tag.like('%' + tag + '%')).order_by('id desc').paginate(page,3)
	else:
		articles=Article.query.order_by('id desc').paginate(int(page),3)
	return render_template('tachilab/show_article.html',articles=articles,category=category,keyword=keyword)	
	
@app.route('/add_article/',methods=['GET','POST'])
def add_article():
	if request.method=='POST':
		form=ArticleForm(request.form)
		category=Category.query.filter_by(id=int(form.category.data)).one()
		article=Article(form.title.data,form.contents.data,category,form.tag.data)
		db.session.add(article)
		db.session.commit()
		return redirect(url_for('show_article'))
	else:
		form=ArticleForm()
	return render_template('tachilab/add_article.html',form=form)

class ArticleForm(Form):
	title=TextField(u'title')
	contents=TextAreaField(u'contents')
	category=SelectField(u'category',choices=Category.show_list())
	tag=TextField(u'tag')

@app.route('/edit_article/',methods=['GET','POST'])
def edit_artice():
	if request.method=='POST':
		form=ArticleForm(request.form)
		#edit_id=request.args.get('id')
		edit_id=request.form['edit_id']
		a=Article.query.filter_by(id=int(edit_id)).one()
		a.title=form.title.data
		a.contents=form.contents.data
		a.category_id=int(form.category.data)
		a.tag=form.tag.data
		db.session.add(a)
		db.session.commit()
		return redirect('/edit_article/')	
	
	edit_id=request.args.get('id','')
	del_id=request.args.get('del_id','')
	if edit_id:
		a=Article.query.filter_by(id=int(edit_id)).one()
		form=ArticleForm()
		form.title.data=a.title
		form.contents.data=a.contents
		form.category.data=str(a.category.id)
		form.tag.data=a.tag
		return render_template('tachilab/edit_form.html',form=form,a=a)

	if del_id:
		a=Article.query.filter_by(id=int(del_id)).one()
		db.session.delete(a)
		db.session.commit()
		return redirect('/edit_article/')

	articles=Article.query.order_by('id desc').all()	
	return render_template('tachilab/edit_article.html',articles=articles)

@app.route('/login/',methods=['GET','POST'])
def login_action():
	form=LoginForm(request.form)
	if request.method=='POST':
		username=request.form['username']
		password=request.form['password']
		user=User.query.filter_by(username=username).one()
		bcrypt=Bcrypt(app)
		if bcrypt.check_password_hash(user.password,password):
			session['user']=user.id
			return redirect(url_for('add_article'))
	return render_template('tachilab/login.html',form=form)	

class LoginForm(Form):
	username=TextField(u'username')
	password=PasswordField(u'password')

@app.route('/logout/')
def logout_action():
	session.pop('user',None)
	return redirect(url_for('show_article'))

if __name__=='__main__':
	app.debug=True
	app.secret_key='hogehoge'
	app.run()
