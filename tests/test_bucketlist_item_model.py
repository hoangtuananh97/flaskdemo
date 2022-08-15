""" unit tests for BucketList items model"""
from app import db
from app.api.model import Users
from app.api.model.bucket_list.bucket import BucketListItems, BucketLists

from .test_base import BaseTestCase


class BucketListTestCase(BaseTestCase):
    """unit tests for BucketList items model"""

    def test_add_bucketlist(self):
        """Ensure that users can add bucket list item"""
        user = Users(username="Jane", password="test123")
        bucketlist = BucketLists(name="Adventure", completed_by=25, owner=user)
        item = BucketListItems(name="Climb Mt.Kilimanjaro", bucket_list=bucketlist)
        db.session.add_all([user, bucketlist, item])
        db.session.commit()
        self.assertTrue(item.id)
        self.assertEqual([item.name, item.completed], ["Climb Mt.Kilimanjaro", False])
