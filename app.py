"""Blogly application."""

from flask import Flask, render_template, redirect, flash, request, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
def home_page():
    """Page for Blogly App"""
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Page to add new user"""
    return render_template('newUser.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
    """Create new user and redirect to home page"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    if not last_name:
        last_name = None
    
    if not image_url:
        image_url = None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<user_id>')
def display_user_details(user_id):
    """Display user detail page"""
    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user)

@app.route('/users/<user_id>/edit')
def edit_user_info(user_id):
    """Edit user form"""
    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def edit_user_details(user_id):
    """Update user info in db and return to user details page"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from db and return to home page"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')
