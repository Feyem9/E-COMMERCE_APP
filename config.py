import os
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


db = SQLAlchemy()

SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:feyem111@127.0.0.1:3306/e_commerce_app?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFCATIONS = False
JWT_SECRET_KEY = 'Feyem111'

MAIL_SERVER= 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'feyemlionel@gmail.com'
MAIL_PASSWORD = 'lujb edfm gnxt mkdy'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = ('E-Commerce App', 'feyemlionel@gmail.com')  # Remplacez par votre nom et email d'envoie
UPLOAD_EXTENSIONS = ['.jpg', '.png' , '.jpeg' , '.avif' , '.webp']
UPLOAD_PATH = "static/image_uploads/"