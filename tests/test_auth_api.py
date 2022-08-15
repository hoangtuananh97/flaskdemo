""" unit tests for authentication api """
import json

from app import create_app, db

from .test_base import BaseTestCase


class TestAuthCase(BaseTestCase):
    """unit tests for authentication api"""

    def setUp(self):
        """initial setup before a test is run"""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(self)
        db.create_all()
        # log in a user
        self.resp = self.client.post(
            "auth/register",
            data=json.dumps(dict(username="testuser", password="testpassword")),
            content_type="application/json",
        )
        self.token = json.loads(self.resp.data.decode())["token"]

    def test_register_user(self):
        """Ensure that users get registered"""
        with self.client:
            data = json.loads(self.resp.data.decode())
            self.assertEqual(self.resp.status_code, 201)
            self.assertEqual(data["message"], "testuser")
            self.assertTrue(data["token"])

    def test_register_user_invalid_json(self):
        """Ensure that error is returned on invalid json"""
        with self.client:
            response = self.client.post(
                "auth/register",
                data=json.dumps(dict()),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual("Invalid payload", data["message"])
            self.assertEqual("Fail", data["status"])
            self.assertIsNone(data["token"])

    def test_register_user_invalid_keys(self):
        """Ensure that error is returned on missing/invalid keys"""
        with self.client:
            response = self.client.post(
                "auth/register",
                data=json.dumps(dict(username="Paul")),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual("Invalid payload", data["message"])
            self.assertEqual("Fail", data["status"])
            self.assertIsNone(data["token"])

    def test_add_duplicate_user(self):
        """Ensure that an error is returned on a duplicate user registration"""
        with self.client:
            response = self.client.post(
                "auth/register",
                data=json.dumps(dict(username="testuser", password="testpassword")),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry username already is taken", data["message"])
            self.assertIn("Fail", data["status"])
            self.assertIsNone(data["token"])

    def test_user_correct_login(self):
        """Ensure that user logs in with correct credentials"""
        with self.client:
            response = self.client.post(
                "auth/login",
                data=json.dumps(dict(username="testuser", password="testpassword")),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Success", data["status"])

    def test_user_incorrect_password(self):
        """Ensure that user doesnt logs in with incorrect credentials"""
        with self.client:
            response = self.client.post(
                "auth/login",
                data=json.dumps(dict(username="testuser", password="testpword")),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Fail", data["status"])

    def test_user_incorrect_username(self):
        """Ensure that user doesnt logs in with incorrect credentials"""
        with self.client:
            response = self.client.post(
                "auth/login",
                data=json.dumps(dict(username="Laura", password="qwerty")),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Fail", data["status"])

    def test_user_reset_password(self):
        """Ensure that user can reset password"""
        with self.client:
            response = self.client.post(
                "auth/reset-password",
                data=json.dumps(
                    dict(
                        username="testuser",
                        old_password="testpassword",
                        new_password="test",
                    )
                ),
                content_type="application/json",
                headers=dict(Authorization="Bearer " + self.token),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data["status"], "Success")
            self.assertTrue(data["token"])

    def test_user_reset_incorrectpassword(self):
        """Ensure that user can reset password"""
        with self.client:
            response = self.client.post(
                "auth/reset-password",
                data=json.dumps(
                    dict(
                        username="testuser",
                        old_password="password",
                        new_password="test",
                    )
                ),
                content_type="application/json",
                headers=dict(Authorization="Bearer " + self.token),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "Fail")
            self.assertIsNone(data["token"])

    def test_user_logout(self):
        """Ensure that users can logout successfully"""
        with self.client:
            response = self.client.get(
                "auth/logout",
                content_type="application/json",
                headers=dict(Authorization="Bearer " + self.token),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "Success")
