#coding: utf-8
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
import smtplib

gmail_address='tatick.tic.tic.tic.tock@gmail.com'
gmail_passwd='tk0131'
gmail_smtp_address='smtp.gmail.com'
gmail_smtp_port=587

from_address='tatick.tic.tic.tic.tock@gmail.com'
to_address=['fixxxer_tachi@yahoo.co.jp','fixxxxxer.tachi@gmail.com']
subject=u'日本語サブジェクト'
body=u'''
ボディも日本語。
改行はだいじょうぶ？??
'''
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
