from sqlalchemy import desc

from app import db
from app.api.model import BucketLists
from app.core.common.common import delete_data, save_data
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


def create_bucketlist(**data):
    bucket_list = BucketLists(**data)
    save_data(bucket_list)


def delete_bucketlist(bucketlist):
    delete_data(bucketlist)


def update_bucketlist(bucketlist, params):
    if params.get("name"):
        bucketlist.name = params.get("name")
    if params.get("complete_by"):
        bucketlist.complete_by = params.get("complete_by")
    db.session.commit()
    return bucketlist


def bucketlist_response(contracts):
    response_data = []
    for item in contracts:
        response_data.append(
            {
                "id": item.id,
                "name": item.name,
                "complete_by": item.complete_by,
                "owner": item.owner,
            }
        )
    return response_data


def get_list_from_filter(input_params):
    page = int(input_params["page"])
    page_size = int(input_params["size"])
    keyword = input_params.get("name", "")
    keyword = "%{}%".format(keyword)
    query = BucketLists.query.all()
    total = query.count()
    if keyword:
        query = query.filter(BucketLists.name.ilike(keyword))
    bucketlists = (
        query.order_by(desc(BucketLists.id))
        .paginate(page=page, per_page=page_size)
        .items
    )
    response_data = bucketlist_response(bucketlists)
    return {
        "items": response_data,
        "page_size": page_size,
        "page": page,
        "total": total,
    }
