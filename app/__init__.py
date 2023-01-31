from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail

#for pythonanywhere
#import mysql.connector

#for localhost
import pymysql


app = Flask(__name__)

#for python anywhere
# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="IronChef",
#     password="Liverp00l001!",
#     hostname="IronChef.mysql.eu.pythonanywhere-services.com",
#     databasename="IronChef$portfolio_website",
# )
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

#for localhost
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1123652:Liverp00l001!@csmysql.cs.cf.ac.uk:3306/c1123652_portfolio'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '879dd461d269f89c799c52abf49af8c59477c445849953e4'

# Uploads/Downloads
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_PATH'] = 'app/static/uploads'
app.config['DOWNLOADS'] ='static\\downloads'

# Mail Perver
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aleccookportfolio@gmail.com'
app.config['MAIL_PASSWORD'] = 'mhhsepxmgsmapqeg'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
mail = Mail(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
moment = Moment(app)

from app import routes, models, errors
from app.views import AdminView
from app.models import User, Post, Computing, Education, Work_experience, Code_examples

# Admin Panel
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Education, db.session))
admin.add_view(AdminView(Work_experience, db.session))
admin.add_view(AdminView(Computing, db.session))
admin.add_view(AdminView(Code_examples, db.session))
