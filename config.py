import os
from flask_sqlalchemy import SQLAlchemy
# from app import index , mail 
# from flask_mail import Message


# MESSAGE = Message
# index.config.from_object('config')
# mail.config.from_object('config')
db = SQLAlchemy()
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Feyem.111@127.0.0.1:3306/e_commerce_app?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFCATIONS = False

MAIL_SERVER= 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'feyemlionel@gmail.com'
MAIL_PASSWORD = 'lujb edfm gnxt mkdy'
MAIL_USE_TLS = True
MAIL_USE_SSL = False

UPLOAD_EXTENSIONS = ['.jpg', '.png' , '.jpeg', '.avif']
UPLOAD_PATH = "static/image_uploads/"