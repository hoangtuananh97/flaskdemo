""" unit tests for BucketList model"""
from app.models import Users, BucketLists
from app import db
from .test_base import BaseTestCase

class BucketListTestCase(BaseTestCase):
    """ unit tests for BucketList model"""
    def test_add_bucketlist(self):
        """ Ensure that user can add bucket list """
        user = Users(username="Peter",password="123")
        bucketlist = BucketLists(name="Career", completed_by=30, owner=user)
        db.session.add_all([user, bucketlist])
        db.session.commit()
        self.assertTrue(bucketlist.id)
        self.assertEqual([bucketlist.name, bucketlist.completed_by], ["Career", 30])
