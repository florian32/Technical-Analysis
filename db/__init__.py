from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    name = db.Column(db.String(30))
    search_history = db.relationship('Search', backref='user', lazy=True)


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(15), nullable=False)
    timestamp = db.Column(db.String(3), nullable=True)
    analysis_types = db.Column(db.String(20), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
