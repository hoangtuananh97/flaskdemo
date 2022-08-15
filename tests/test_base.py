""" base set up testing utilities """

import unittest

from app import create_app, db


class BaseTestCase(unittest.TestCase):
    """basic configuration for unit tests"""

    def setUp(self):
        """initial setup before a test is run"""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(self)
        db.create_all()

    def tearDown(self):
        """executes  after a test is run"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
