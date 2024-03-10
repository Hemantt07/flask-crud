from application import app
from flask import render_template
from flask_mail import Mail, Message

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '583e5bc9893a58'
app.config['MAIL_PASSWORD'] = '7d5d4d7079a6bc'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'hemantt079@gmail.com'

mail = Mail(app)

def send_registration_email(email, name):
    msg = Message('Welcome to Our Website!', recipients=[email])
    msg.html = render_template('mails/registration_email.html', name=name)
    mail.send(msg)