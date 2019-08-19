#!flask/bin/python
import os
import unittest

from config import basedir
from sqlalchemy import exc
from app import db, mail
from app.models import (User, Post, Rapper, import_user, delete_user,
    import_post, clear_posts)
from app.scraper import login, generate_subject, send_email

email = "fake@gmail.com"
emails = ["fake@gmails.com"]


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    #################################
    #Checking Page Status Unit Tests#
    #################################
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_unsubscribe_page(self):
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.app.get('/unsub', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_success_page(self):
        response = self.app.get('/success', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    ##################################
    #Checking DB Functions Unit Tests#
    ##################################
    
    def test_add_User(self):
        user_email = "myfakeemail@gmail.com"
        import_user(user_email, "1")
        self.assertTrue(User.query.filter_by(email=user_email).first())

    def test_remove_User_valid(self):
        user_email = "myfakeemail@gmail.com"
        import_user(user_email, "1")
        delete_user(user_email)
        self.assertFalse(User.query.filter_by(email=user_email).first())

    def test_remove_User_invalid(self):
        self.assertRaises(exc.SQLAlchemyError, delete_user("fake@gmail.com"))

    def test_add_Post(self):
        post_id = "12345"
        import_post(post_id)
        self.assertTrue(Post.query.filter_by(post_id=post_id).first())

    def test_wipe_Post(self):
        post_id_1 = "12345"
        post_id_2 = "54321"
        import_post(post_id_1)
        import_post(post_id_2)
        clear_posts()
        self.assertFalse(Post.query.filter_by(post_id=post_id_1).first())


    ####################################
    #Checking PRAW Functions Unit Tests#
    ####################################
    #def test_praw_login(self):


    #def test_praw_scrape(self):

    #####################################
    #Checking Email Functions Unit Tests#
    #####################################

    def test_send_email(self):
        user = User(email=email, rapper_id="1")
        import_user(user.email, user.rapper_id)
        subscribed = User.query.filter(User.rapper_id == "1")
        with mail.record_messages() as outbox:
            send_email(subscribed, "Kanye West", "1234")
            assert len(outbox) == 1
            assert outbox[0].subject == "Fresh Kanye West Awaits You"

    def test_generate_subject(self):
        self.assertEqual("Fresh Young Thug Awaits You", generate_subject("Young Thug"))


if __name__ == '__main__':
    unittest.main()
