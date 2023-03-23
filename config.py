import os

DEBUG = True
SECRET_KEY = 'askdoamsodmsaojsd'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
# MAIL_USE_SSL = True
MAIL_USE_TLS = True

MAIL_USERNAME = os.getenv('MAIL_LOGIN')
MAIL_PASSWORD = os.getenv('MAIL_PASS')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_LOGIN')