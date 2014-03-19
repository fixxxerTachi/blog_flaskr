#coding:utf-8
import sys
from flask import Flask,render_template,request,redirect,url_for,session
from admin_models import Product,Order,Status,Brand,Admin,Type,Color,User
from admin_database import db_session
from sqlalchemy.sql.expression import desc
from sqlalchemy.orm import subqueryload,joinedload,contains_eager
from wtforms import Form,TextField,PasswordField,IntegerField,SelectField,FileField,TextAreaField
from flaskext.bcrypt import Bcrypt
from werkzeug import secure_filename
import datetime
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
import smtplib

app=Flask(__name__)
app.secret_key='ghoehgeoh'
@app.before_request
def check_login():
	if request.path != '/login/':
		if not 'admin_id' in session:
			return redirect('/login/')
@app.route('/')
def show_menu():
	return render_template('admin_menu.html')

@app.route('/shipment/',methods=['POST','GET'])
def shipment():
	if request.method=='POST':
		for v in request.form:
			'''v : 'shipment-743-0'
			'''
			splited=v.split('-')
			order_id=int(splited[1])
			product_id=int(splited[2])
			order=Order.query.filter_by(id=order_id).one()
			#order.products[key].status_id=int(request.form[v])
			for p in order.products:
				if p.product.id==product_id:
					if p.status_id is not int(request.form[v]):
						p.status_id=int(request.form[v])
						db_session.add(order)
						db_session.commit()

		q_str=request.args.get('status','')
		if q_str:
			url='/shipment/?status=' + q_str
		else:
			url='/shipment/'
		return redirect(url)
	elif request.args.get('status')=='accepted':
		orders=Order.query.options(joinedload(Order.products)).filter(Order.products.any(status_id=1)) \
			.order_by(desc(Order.created_at)).all()
	elif request.args.get('status')=='prepared':
		orders=Order.query.options(joinedload(Order.products)).filter(Order.products.any(status_id=2)) \
			.order_by(desc(Order.created_at)).all()
	else:
		#orders=Order.query.order_by(desc(Order.created_at)).all()
		orders=Order.query.options(joinedload(Order.products)).order_by(desc(Order.created_at)).all()

	statuses=Status.query.order_by(Status.id).all()
	return render_template('admin_shipment.html',orders=orders,statuses=statuses)

@app.route('/arrival/',methods=['GET','POST'])
def arrival():
	if request.method=='POST':
		for v in request.form:
			if request.form[v]:
				product_id=int(v.split('quantity')[1])
				p=Product.query.filter_by(id=product_id).one()
				p.quantity=p.quantity + int(request.form[v])
				db_session.add(p)
				db_session.commit()
		products=Product.query.order_by(desc(Product.quantity)).order_by(Product.id).all()

	if request.method=='GET':
		brand_id=request.args.get('brand','')
		if brand_id:
			products=Product.query.filter(Product.brand_id==int(brand_id)).all()
		else:
			products=Product.query.order_by(desc(Product.quantity)).order_by(Product.id).all()

	brands=Brand.query.all()
	return render_template('admin_arrival.html',products=products,brands=brands)

@app.route('/login/',methods=['POST','GET'])
def login():
	form=LoginForm(request.form)
	if request.method=='POST' and form.validate():
		try:
			admin=Admin.query.filter_by(username=request.form['username']).one()
			bcrypt=Bcrypt(app)
			if bcrypt.check_password_hash(admin.password,request.form['password']):
				session['admin_id']=admin.id
				return redirect('/')
			else:
				return render_template('admin_login.html',form=form,data='no password')
		except: 
			return render_template('admin_login.html',form=form,data='no username')
	return render_template('admin_login.html',form=form,data='')

@app.route('/logout/')
def logout():
	session.pop('admin_id',None)
	return redirect('/login/')

class LoginForm(Form):
	username=TextField(u'ユーザー名')
	password=PasswordField(u'パスワード')

@app.route('/add_product/',methods=['POST','GET'])
def add_product():
	if request.method=='POST':
		f=ProductForm(request.form)
		data=request.form
		product=Product()
		product.brand_id=data['brand']
		product.color_id=data['color']
		product.price=data['price']
		product.type_id=data['type']
		product.quantity=data['quantity']
		product.created=datetime.datetime.now()
		product.modified=datetime.datetime.now()
		db_session.add(product)
		db_session.commit()
		brand=Brand.query.filter_by(id=data['brand']).one()
		color=Color.query.filter_by(id=data['color']).one()
		product.code='%s-%s-%d' % (brand.code,color.code,product.id)
		product.img='%s-%s-%d.jpg' % (brand.name,color.code,product.id)
		db_session.add(product)
		db_session.commit()
		img=request.files['img']	
		img.save('/home/tachi/laravel4.0/public/images/brands/'+ brand.code + '/' + product.img)
	else:
		f=ProductForm()
	return render_template('add_product.html',f=f)

class ProductForm(Form):
	brand=SelectField(u'ブランド',choices=Brand.show_list())
	color=SelectField(u'color',choices=Color.show_list())
	price=IntegerField(u'価格')
	type=SelectField(u'type',choices=Type.show_list())
	quantity=IntegerField(u'数量')
	img=FileField(u'商品画像')

@app.route('/mail_maga/' ,methods=['POST','GET'])
def send_mail():
	users=User.query.all()
		
	if request.method=='POST':
		form=MailForm(request.form)
		data=request.form
		gmail_address='tatick.tic.tic.tic.tock@gmail.com'
		gmail_passwd='tk0131'
		gmail_smtp_address='smtp.gmail.com'
		gmail_smtp_port=587

		from_address='tatick.tic.tic.tic.tock@gmail.com'
		to_address=[user.email for user in users]
		#to_address=['fixxxer_tachi@yahoo.co.jp','fixxxxxer.tachi@gmail.com']
		subject=data['subject']
		body=data['body']
		msg=MIMEText(body.encode('iso-2022-jp'),'plain','iso-2022-jp')
		msg['From']=from_address
		msg['To']=','.join(to_address)
		msg['Date']=formatdate()
		msg['Subject']=Header(subject.encode('iso-2022-jp'),'iso-2022-jp')
		smtpobj=smtplib.SMTP(gmail_smtp_address,gmail_smtp_port)
		smtpobj.ehlo()
		smtpobj.starttls()
		smtpobj.ehlo()
		smtpobj.login(gmail_address,gmail_passwd)
		for address in to_address:
			smtpobj.sendmail(from_address,address,msg.as_string())
		smtpobj.close()
		return redirect('/mail_maga/')
	else:
		form=MailForm()	
	return render_template('send_mail.html',form=form,users=users)

class MailForm(Form):
	subject=TextField(u'タイトル')
	body=TextAreaField(u'本文')



if __name__=='__main__':
	app.debug=True
	app.run()
