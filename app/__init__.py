from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask import Flask


app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail()
mail.init_app(app)

from app.controllers import default
from app.models import tables