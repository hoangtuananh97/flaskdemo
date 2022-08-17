from datetime import datetime

from app.extensions.database import db


class BaseModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.id)

    @classmethod
    def get_all(cls, delete=True):
        instance = cls().query
        if delete:
            instance = instance.filter_by(deleted_date=None)
        return instance

    @classmethod
    def get_by_id(cls, instance_id):
        """Get by id"""
        instance = cls().query.filter_by(id=instance_id, deleted_date=None).first()
        return instance

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class BaseModelMeta(BaseModel):
    __abstract__ = True

    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(db.String(100), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    updated_by = db.Column(db.String(100), nullable=True)


class BaseModelMetadata(BaseModelMeta):
    __abstract__ = True

    deleted_date = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.String(100), nullable=True)

    def delete(self, **kwargs):
        if user := kwargs.get("users", None):
            self.deleted_by = user
            self.deleted_date = datetime.utcnow()
