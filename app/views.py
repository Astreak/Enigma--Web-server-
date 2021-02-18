from flask import *
from app import app
from app import *
@app.route('/')
def home():
        email=dict(session).get('email',None)
        if email!=None:
                return render_template("home.html",name=session.get('username',None))
        else:
                flash('you have to login first')
                return redirect(url_for('Login'))

@app.route('/about')
def about():
        return "<h1><b><center> AboutPage </center></b></h1>"