from application import app

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '583e5bc9893a58'
app.config['MAIL_PASSWORD'] = '7d5d4d7079a6bc'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
