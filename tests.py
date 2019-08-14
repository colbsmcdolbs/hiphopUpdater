#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Rapper


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


if __name__ == '__main__':
    unittest.main()
