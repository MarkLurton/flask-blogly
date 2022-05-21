"""Blogly application."""

from flask import Flask, render_template, redirect, flash, request, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
def home_page():
    """Page for Blogly App"""
    users = User.query.all()
    posts = Post.recent_posts()
    return render_template('index.html', users=users, posts=posts)

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

    return render_template('editUser.html', user=user)

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

@app.route('/users/<user_id>/posts/new')
def show_new_post_form(user_id):
    """Show add post form for selected user"""

    user = User.query.get_or_404(user_id)
    return render_template('newPost.html', user=user)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    """Submit new post and redirect to user details page"""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>')
def display_post(post_id):
    """Display post of given post_id"""

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<post_id>/edit')
def edit_post_form(post_id):
    """Display edit post form"""

    post = Post.query.get_or_404(post_id)
    return render_template('editPost.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Edit post and redirect back to post page"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    

    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post and return to user page"""
    
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')