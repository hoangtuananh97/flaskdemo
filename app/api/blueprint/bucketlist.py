from flask_restx import Namespace


class BucketListsBlueprint:
    api = Namespace("bucketlists", description="api bucketlist")
