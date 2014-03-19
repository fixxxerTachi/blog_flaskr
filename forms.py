from flask import Flask,render_template,request
from wtforms import Form,BooleanField,TextField,PasswordField,validators
app=Flask(__name__)

class RegistrationForm(Form):
	username=TextField('Username',[validators.Length(min=4,max=25)])
	email=TextField('Email Address',[validators.Length(min=6,max=35)])
	password=PasswordField('New Password',[
		validators.Required(),
		validators.EqualTo('confirm',message='Passwords must match')
	])
	confirm=PasswordField('Repeat Password')
	accecpt_tos=BooleanField('I accept the TOS',[validators.Required()])

@app.route('/register',methods=['GET','POST'])
def register():
	form=RegistrationForm(request.form)
	if request.method=='POST':
		data=request.form
		return render_template('register.html',form=form,data=data)
	return render_template('register.html',form=form)

if __name__=='__main__':
	app.debug=True
	app.run()
