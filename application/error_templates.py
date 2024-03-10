from application import app
from flask import render_template

@app.errorhandler(404)
def not_found_error():
    return render_template( 'errors/404.html' )

@app.errorhandler(500)
def server_error():
    return render_template( 'errors/500.html' )

