import smtplib
smtp=smtplib.SMTP('smtp.gmail.com',587)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login('tatick.tic.tic.tic.tock@gmail.com','tk0131')
smtp.sendmail('tatick.tic.tic.tic.tock@gmail.com','fixxxer_tachi@yahoo.co.jp','from flask')
smtp.quit()

