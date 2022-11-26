from flask import Flask, request, Blueprint, url_for, jsonify
from flask_cors import CORS
from response.http_response import *
from config.swagger import template, swagger_config
from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.exc import *
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
CORS(app= app)
Swagger(app=app, config= swagger_config, template= template)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'pemrogramanmobiledapeta'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///kasir.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SWAGGER'] = {
    'title' : 'Kasir REST API Pemrograman Mobile',
    'uiversion' : 3
}


BASE_URL_API = '/api/kasir'


db.create_all()