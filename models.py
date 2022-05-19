"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to app to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """SQLAlchemy users model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(25),
                            nullable = False)

    last_name = db.Column(db.String(25),
                            nullable = True)

    image_url = db.Column(db.Text,
                            nullable = True,
                            default = 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')
