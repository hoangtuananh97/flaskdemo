""" BucketList Models """
from app import db
from app.api.model.base import BaseModelMeta


class BucketLists(BaseModelMeta):
    """Model for bucket lists"""

    __tablename__ = "bucketlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    completed_by = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    bucket_lists_items = db.relationship(
        "BucketListItems",
        backref="bucket_list",
        lazy="dynamic",
        cascade="delete, delete-orphan",
    )

    def to_json(self):
        """Convert bucket list model to json format"""
        json_data = {
            "id": self.id,
            "name": self.name,
            "completed_by": self.completed_by,
            "items": [item.to_json() for item in self.bucket_lists_items.all()],
        }
        return json_data


class BucketListItems(BaseModelMeta):
    """Model for bucket list items"""

    __tablename__ = "bucketlistitems"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlists.id"))

    def to_json(self):
        """Convert bucket list item model to json format"""
        json_data = {"id": self.id, "name": self.name, "completed": self.completed}
        return json_data
