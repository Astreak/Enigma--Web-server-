from flask import *
from flask_sqlalchemy import *
from flask_login import LoginManager,current_user,login_user,login_required,UserMixin,logout_user
from app import app

db=SQLAlchemy(app)

class Drank(db.Model,UserMixin):
        id=db.Column(db.Integer,primary_key=True)
        username=db.Column(db.String(100),unique=True,nullable=False)
        email=db.Column(db.String(100),unique=True,nullable=False)
        password=db.Column(db.String(1000),unique=False,nullable=False)
        links=db.Column(db.String(500000),unique=False,nullable=True)
        gid=db.Column(db.String(100000),unique=True,nullable=True)
        def get_json(self):
                A=json.dumps({
                        "Username":self.username,
                        "Email":self.email,
                        "Password":self.password,
                        "Lists":self.Lists
                })
                return A

db.create_all()
db.session.commit()

        
        


