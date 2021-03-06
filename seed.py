"""Seed file to make sample data for pets db"""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
mark = User(first_name='Mark', last_name='Lurton')
braden = User(first_name='Braden', last_name='Schiller')
norma = User(first_name="Norma", last_name='Noonan')
cher = User(first_name="Cher")

# Add tags 
whoop = Tag(name='whoop')
howdy = Tag(name='howdy')
bloop = Tag(name='bloop')

#Add posts
p = Post(title='1st Post', content='This is my first post! Will it work?', user_id=1)

#Add posts tags
pt = PostTag(post_id=1, tag_id=1)

# Add new objects to session, so they'll persist
db.session.add(mark)
db.session.add(braden)
db.session.add(norma)
db.session.add(cher)
db.session.add(whoop)
db.session.add(howdy)
db.session.add(bloop)

# Commit--otherwise, this never gets saved!
db.session.commit()

# Now add posts and commit
db.session.add(p)
db.session.commit()

# Add post tags
db.session.add(pt)
db.session.commit()