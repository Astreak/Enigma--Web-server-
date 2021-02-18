from flask import *
from flask_sqlalchemy import *
from flask_migrate import Migrate
from flask_login import LoginManager,current_user,login_user,login_required,UserMixin,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

import sys

app =Flask(__name__,static_folder="static")
app.config.from_object("config.DevelopmentEnv")
#print(app.config)
from app.database import *

from app import views
from app import authentication
from app import api
