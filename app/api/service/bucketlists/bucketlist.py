from app.api.model import BucketLists
from app.core.exceptions.not_found import NotFoundException


def get_bucketlist_detail(bucketlist_id, user_id):
    bucketlist = BucketLists.query.filter_by(id=bucketlist_id, owner_id=user_id).first()
    if not bucketlist:
        raise NotFoundException(message="Item doesn't exist")
    return {
        "id": bucketlist.id,
        "name": bucketlist.name,
        "complete_by": bucketlist.completed_by,
        "owner": bucketlist.owner,
    }
