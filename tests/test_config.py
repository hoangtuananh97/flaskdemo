""" unit tests for config.py """

from flask import current_app

from .test_base import BaseTestCase


class ConfigTestCase(BaseTestCase):
    """unit tests for basic config and setup"""

    def test_app_exists(self):
        """test if app exists"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """test if app config is testing"""
        self.assertFalse(self.app.config["DEBUG"])
        self.assertEqual(4, self.app.config["BCRYPT_LOG_ROUNDS"])
        self.assertEqual(5, self.app.config["TOKEN_EXPIRATION_SECONDS"])
        self.assertEqual(0, self.app.config["TOKEN_EXPIRATION_DAYS"])
