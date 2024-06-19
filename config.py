import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Feyem.111@127.0.0.1:3306/e_commerce_app'
SQLALCHEMY_TRACK_MODIFCATIONS = False

MAIL_SERVER= 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'feyemlionel@gmail.com'
MAIL_PASSWORD = 'lujb edfm gnxt mkdy'
MAIL_USE_TLS = True
MAIL_USE_SSL = False