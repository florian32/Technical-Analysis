from flask import Flask, jsonify
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

from config import config

db = SQLAlchemy()


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
    sma = db.Column(db.Boolean, nullable=False)
    res = db.Column(db.Boolean, nullable=False)
    formations = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
