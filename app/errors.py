from flask import render_template
from app import app, db

# Code to handle 404 and 500 errors
# Taken from The Flask Mega Tutorial by Miguel Grinberg
# Accessed on 18/01/2023
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
# End of referenced code