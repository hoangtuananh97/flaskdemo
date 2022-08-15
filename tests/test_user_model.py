""" unit tests for the user model """
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Users
from app.utils import add_user
from .test_base import BaseTestCase


class UsersTestCase(BaseTestCase):
    """ unit tests for the user model """

    def test_add_user(self):
        """ Ensure that user is added """
        user = add_user("Paul", "password")
        self.assertTrue(user.id)
        self.assertEqual(user.username, "Paul")

    def test_duplicate_users(self):
        """ Ensure that duplicate users are not  added """
        add_user("Paul", "password")
        with self.assertRaises(IntegrityError):
            add_user("Paul", "test")

    def test_missing_password(self):
        """ Ensure that an error is returned on missing password """
        with self.assertRaises(TypeError):
            add_user("Paul")

    def test_missing_username(self):
        """ Ensure that an error is returned on missing username """
        with self.assertRaises(TypeError):
            user = Users(password="Paul")

    def test_encode_auth_token(self):
        """ Ensure that authentication token is returned after user registration """
        user = add_user(username="Paul", password="password")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        """ Ensure that authentication token is correctly decoded """
        user = add_user(username="Paul", password="password")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(Users.decode_auth_token(auth_token), user.id)
