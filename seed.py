"""Seed file to make sample data for pets db"""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
mark = User(first_name='Mark', last_name='Lurton')
braden = User(first_name='Braden', last_name='Schiller')
norma = User(first_name="Norma", last_name='Noonan')
cher = User(first_name="Cher")

# Add new objects to session, so they'll persist
db.session.add(mark)
db.session.add(braden)
db.session.add(norma)
db.session.add(cher)

# Commit--otherwise, this never gets saved!
db.session.commit()
