from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        Post.query.delete()

        post = Post(title="Test_Title", content="Test_Content", user_id=user.id)

        db.session.add(post)
        db.session.commit()


        self.user_id = user.id
        self.user = user

        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""
        self.post.title = "Test_Title"
        self.post.content = "Test_Content"

        db.session.add(self.post)
        db.session.commit()

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)
            self.assertIn(self.user.first_name, html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Test2", "last_name": "User2", "image_url": "data:image/jpeg;base64,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"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2 User2", html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit User Info", html)
    
    def test_show_new_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post for Test User', html)
    
    def test_submit_new_post(self):
        with app.test_client() as client:
            d = { "title" : "Test_Title_2", "content" : "Test_Content_2", "user_id" : self.user.id }
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test_Title_2', html)
    
    def test_display_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test_Title', html)
    
    def test_edit_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Post', html)
    
    def test_edit_post(self):
        with app.test_client() as client:
            d = { "title" : "Test_Edit", "content" : "Test_Content"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test_Edit', html)
