""" unit tests for the bucketlist api """
import json
from app import create_app, db
from .test_base import BaseTestCase


class TestBucketListCase(BaseTestCase):
    """ unit tests for the bucketlist api """

    def setUp(self):
        """initial setup before a test is run """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(self)
        db.create_all()
        # log in a user
        resp = self.client.post(
            'auth/register',
            data=json.dumps(
                dict(username='testuser', password='testpassword')),
            content_type='application/json'
        )
        self.token = json.loads(resp.data.decode())['token']
        # create bucket list
        self.response = self.client.post(
            'bucketlists',
            data=json.dumps(dict(name="Career", completed_by=30)),
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )
        # create bucket list items
        self.client.post(
                'bucketlists/1/items',
                data=json.dumps(dict(name="Become a Partner")),
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
                )

    def test_create_bucket_lists(self):
        """ Ensure that bucketlists can be created and retrieved """
        with self.client:
            data = json.loads(self.response.data.decode())
            self.assertEqual(self.response.status_code, 201)
            self.assertEqual(data['status'], "Success")
            get_response = self.client.get(
                'bucketlists',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertDictEqual(data, {'bucketlists': [{
                "id": 1,
                "name": "Career",
                "completed_by": 30,
                "items": [{"completed": False,"id": 1, "name": "Become a Partner"}]
            }]})

    def test_no_auth_token(self):
        """ Ensure that error is returned with no headers """
        with self.client:
            response = self.client.post(
                'bucketlists',
                data=json.dumps(dict(name="Career", completed_by=30)),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide valid auth Token')

    def test_get_bucketlists_with_id(self):
        """ Ensure that buckelists with data can be retrieved using IDs """
        with self.client:
            response = self.client.get(
                'bucketlists/1',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {'bucketlist': {
                "id": 1,
                "name": "Career",
                "completed_by": 30,
                "items": [{"completed": False,"id": 1, "name": "Become a Partner"}]
            }})

    def test_update_bucketlists_with_id(self):
        """ Ensure that buckelists with data can be updated using IDs """
        with self.client:
            response = self.client.put(
                'bucketlists/1',
                data=json.dumps(dict(name="Adventure", completed_by=25)),
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {'bucketlist': {
                "id": 1,
                "name": "Adventure",
                "completed_by": 25,
                "items": [{"completed": False,"id": 1, "name": "Become a Partner"}]
            }})

    def test_delete_bucketlists_with_id(self):
        """ Ensure that buckelists with data can be deleted using IDs """
        with self.client:
            response = self.client.delete(
                'bucketlists/1',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {'bucketlist': 1, 'message': 'bucketlist successfully deleted'})

    def test_create_bucketlist_item(self):
        """ Ensure that bucketlist items can be added and retrieved """
        with self.client:
            response = self.client.post(
                'bucketlists/1/items',
                data=json.dumps(dict(name="Become a Jedi")),
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
                )
            data = json.loads(response.data.decode())
            self.assertDictEqual(data, {
                'status': 'Success',
                'bucketlist': {
                    "id": 1,
                    "name": "Career",
                    "completed_by": 30,
                    "items": [
                        {'completed': False, 'id': 1, 'name': 'Become a Partner'},
                        {'completed': False, 'id': 2, 'name': 'Become a Jedi'}
                        ]
                }})

    def test_delete_bucketlists_item(self):
        """ Ensure that buckelist items can be deleted"""
        with self.client:
            response = self.client.delete(
                'bucketlists/1/items/1',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {
                'item': 1,
                'message': 'Item successfully deleted',
                'bucketlist': {
                    "id": 1,
                    "name": "Career",
                    "completed_by": 30,
                    "items": []
                }
            })

    def test_update_bucketlists_items(self):
        """ Ensure that buckelists items can be updated"""
        with self.client:
            response = self.client.put(
                'bucketlists/1/items/1',
                data=json.dumps(dict(name="Adventure", completed=True)),
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {
                'bucketlist': {
                    "id": 1,
                    "name": "Career",
                    "completed_by": 30,
                    "items": [{'completed': True, 'id': 1, 'name': 'Adventure'}]
                }})
    def test_bucketlist_search(self):
        """ Ensure that search queries are executed """
        with self.client:
            response = self.client.get(
                'bucketlists?q=career',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {'search_results': [{
                "id": 1,
                "name": "Career",
                "completed_by": 30,
                "items": [{"completed": False,"id": 1, "name": "Become a Partner"}]
            }]})

    def test_pagination(self):
        """ Ensure that pagination works as expected """
        bucketlists = [
            {"name": "Adventure", "completed_by":25},
            {"name": "Shopping", "completed_by":28},
            {"name": "Health", "completed_by":40}
        ]
        with self.client:
            for item in bucketlists:
                self.client.post(
                    'bucketlists',
                    data=json.dumps(item),
                    content_type="application/json",
                    headers=dict(Authorization='Bearer ' + self.token)
                )
            response = self.client.get(
                'bucketlists?limit=3',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(3, len(data['bucketlists']))
