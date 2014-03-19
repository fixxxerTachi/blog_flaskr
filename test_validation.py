#coding: utf-8
from wtforms import Form,TextField,validators
from werkzeug.datastructures import MultiDict

class MyForm(Form):
	first_name=TextField(u'First_Name',validators=[validators.required(message=u'必須入力です')])
	last_name=TextField(u'Last_Name',validators=[validators.optional()])
	def validate_last_name(form,field):
		if field.data == 'a':
			raise validators.ValidationError(u'aは入力しないでください')

data=MultiDict([('first_name',''),('last_name','a')])
form=MyForm(data)
form.validate()
print form.errors
