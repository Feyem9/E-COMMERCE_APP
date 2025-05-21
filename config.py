import os
from flask_sqlalchemy import SQLAlchemy# type: ignore 
from datetime import timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity # type: ignore


db = SQLAlchemy()

SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:feyem111@127.0.0.1:3306/e_commerce_app?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFCATIONS = False
JWT_SECRET_KEY = 'Feyem111'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

MAIL_SERVER= 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'feyemlionel@gmail.com'
# MAIL_PASSWORD = 'lujb edfm gnxt mkdy'
# MAIL_PASSWORD = 'frsz fiuh jhyl wdhy'
MAIL_PASSWORD = 'fduc lyef pjcb hozb'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
# MAIL_DEFAULT_SENDER = ('E-commerce-APP', 'feyemlionel@gmail.com')  # Remplacez par votre nom et email d'envoie
MAIL_DEFAULT_SENDER = 'feyemlionel@gmail.com'
UPLOAD_EXTENSIONS = ['.jpg', '.png' , '.jpeg' , '.avif' , '.webp']
UPLOAD_PATH = "static/image_uploads/"


PAYUNIT_BASE_URL = "https://gateway.payunit.net"
PAYUNIT_INITIATE_URL = f"{PAYUNIT_BASE_URL}/api/gateway/initialize"
PAUNIT_CONTENT_TYPE = "application/json"
PAYUNIT_AUTHORIZATION ="Basic YWVmNjEzMTgtMGM1Ni00NzVlLTg1NDAtNWYyNWEwMTFmMzkxOjc2NDc2OGQyLTRjYjItNGQ1Ny1hMGVjLWFiZjg0YjAwYzI1Yg=="
PAYUNIT_X_API_KEY ="sand_RX539gKTAipaIomZNk3qjAfr9lvQtK"
PAYUNIT_MODE = "SANDBOX"
