""" view functions for bucketlist """
from flask import Blueprint, request, jsonify
from app.utils import login_required
from app.models import BucketLists, BucketListItems
from app import db

bucketlist_blueprint = Blueprint('bucketlists', __name__)


@bucketlist_blueprint.route('', methods=['POST'])
@login_required
def post_bucketlist(user):
    """ Create bucketlists
    ---
    tags:
      - "bucketlists"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
      - in: "body"
        name: "body"
        description: "bucketlist and the age of completion"
        required: true
        schema:
          type: "object"
          required:
          - "name"
          - "completed_by"
          properties:
            name:
              type: "string"
            completed_by:
              type: "integer"
    responses:
        200:
          description: "successful operation"
        400:
          description: "Invalid Payload"
    """
    post_data = request.get_json()
    name = post_data.get('name')
    completed_by = post_data.get('completed_by')
    blist = BucketLists(name=name, completed_by=completed_by, owner=user)
    db.session.add(blist)
    db.session.commit()
    reponse_object = {
        'status': 'Success',
        'bucketlist': blist.to_json()
    }
    return jsonify(reponse_object), 201


@bucketlist_blueprint.route('', methods=['GET'])
@login_required
def get_bucketlist(user):
    """ Retrieve bucketlists
    ---
    tags:
      - "bucketlists"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
    responses:
        200:
            description: "successful operation"
    """
    q = request.args.get('q')
    limit = request.args.get('limit')
    # add pagination support using a limit parameter
    if limit:
        bucketlists = BucketLists.query.filter_by(owner=user).limit(int(limit))
        return jsonify({'bucketlists': [bucketlist.to_json() for bucketlist in bucketlists]})
    elif q:
        # api searching based on name attribute
        bucketlists = BucketLists.query.filter(
            BucketLists.name.ilike("%" + q + "%"), BucketLists.owner == user).all()
        return jsonify({'search_results': [bucketlist.to_json() for bucketlist in bucketlists]})
    # get request without search argument
    bucketlists = BucketLists.query.filter_by(owner=user)
    return jsonify({'bucketlists': [bucketlist.to_json() for bucketlist in bucketlists]})


@bucketlist_blueprint.route('/<int:bucketlist_id>', methods=['GET'])
@login_required
def retrive_bucketlist(user, bucketlist_id):
    """ Retrieve bucketlist based  on its ID
    ---
    tags:
      - "bucketlists"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "Item doesn't exist"
    """
    bucketlist = BucketLists.query.filter_by(
        id=bucketlist_id, owner=user).first()
    if bucketlist:
        return jsonify({'bucketlist': bucketlist.to_json()})
    return jsonify({"status": "Error", "message": "Item doesn't exist"}), 404


@bucketlist_blueprint.route('/<int:bucketlist_id>', methods=['DELETE'])
@login_required
def del_bucketlist(user, bucketlist_id):
    """ Delete bucketlist based  on its ID
    ---
    tags:
      - "bucketlists"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "Item doesn't exist"
    """
    bucketlist = BucketLists.query.filter_by(
        id=bucketlist_id, owner=user).first()
    if bucketlist:
        id = bucketlist.id
        db.session.delete(bucketlist)
        db.session.commit()
        return jsonify({'bucketlist': id, 'message': 'bucketlist successfully deleted'})
    return jsonify({"status": "Error", "message": "Item doesn't exist"}), 404


@bucketlist_blueprint.route('/<int:bucketlist_id>', methods=['PUT'])
@login_required
def update_bucketlist(user, bucketlist_id):
    """ Update bucketlist based on its ID
    ---
    tags:
      - "bucketlists"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
      - in: "body"
        name: "body"
        description: ""
        required: true
        schema:
          type: "object"
          required:
          - "name"
          - "completed_by"
          properties:
            name:
              type: "string"
            completed_by:
              type: "integer"
    responses:
        200:
          description: "successful operation"
        400:
          description: "Item doesn't exist"
    """
    bucketlist = BucketLists.query.filter_by(
        id=bucketlist_id, owner=user).first()
    if bucketlist:
        put_data = request.get_json()
        name = put_data.get('name')
        completed_by = put_data.get('completed_by')
        bucketlist.name = name
        bucketlist.completed_by = completed_by
        db.session.add(bucketlist)
        db.session.commit()
        return jsonify({'bucketlist': bucketlist.to_json() })
    return jsonify({"status": "Error", "message": "Item doesn't exist"}), 404


@bucketlist_blueprint.route('/<int:bucketlist_id>/items', methods=['POST'])
@login_required
def create_bucketlist_item(user, bucketlist_id):
    """ Create a new bucket list item
    ---
    tags:
      - "bucketlists items"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
      - in: "body"
        name: "body"
        description: ""
        required: true
        schema:
          type: "object"
          required:
          - "name"
          properties:
            name:
              type: "string"
    responses:
        200:
          description: "successful operation"
        400:
          description: "Item doesn't exist"
    """
    bucketlist = BucketLists.query.filter_by(
        id=bucketlist_id, owner=user).first()
    if bucketlist:
        post_data = request.get_json()
        item = BucketListItems(name=post_data.get(
            "name"), bucket_list=bucketlist)
        db.session.add(item)
        db.session.commit()
        return jsonify({'status': 'Success', 'bucketlist': bucketlist.to_json()}), 201
    return jsonify({"status": "Error", "message": "Item doesn't exist"}), 404


@bucketlist_blueprint.route('/<int:bucketlist_id>/items/<int:item_id>', methods=['PUT'])
@login_required
def edit_bucketlist_item(user, bucketlist_id, item_id):
    """ Edit bucket list item
    ---
    tags:
      - "bucketlists items"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
      - in: "body"
        name: "body"
        description: ""
        required: true
        schema:
          type: "object"
          required:
          - "name"
          properties:
            name:
              type: "string"
            completed:
              type: "boolean"
    responses:
        200:
          description: "successful operation"
        404:
          description: "Item doesn't exist"
    """
    bucketlist = BucketLists.query.filter_by(
        id=bucketlist_id, owner=user).first()
    item = BucketListItems.query.filter_by(
        id=item_id, bucket_list=bucketlist).first()
    if item:
        put_data = request.get_json()
        item.name = put_data.get('name')
        item.completed = put_data.get('completed')
        db.session.add(item)
        db.session.commit()
        return jsonify({'bucketlist': bucketlist.to_json()})
    return jsonify({"status": "Error", "message": "Item doesn't exist"}), 404


@bucketlist_blueprint.route('/<int:bucketlist_id>/items/<int:item_id>', methods=['DELETE'])
@login_required
def del_bucketlist_item(user, bucketlist_id, item_id):
    """ Delete bucket list item
    ---
    tags:
      - "bucketlists items"
    parameters:
      - name: "Authorization"
        in: "header"
        description: "Token of a logged in user"
        required: true
        type: "string"
    responses:
        200:
          description: "successful operation"
        404:
          description: "Item doesn't exist"
    """
    bucketlist = BucketLists.query.filter_by(
        id=bucketlist_id, owner=user).first()
    item = BucketListItems.query.filter_by(
        id=item_id, bucket_list=bucketlist).first()
    if item:
        id = item.id
        db.session.delete(item)
        db.session.commit()
        return jsonify({'item': id,
                        'message': 'Item successfully deleted',
                        'bucketlist':bucketlist.to_json()
                       })
    return jsonify({"status": "Error", "message": "Item doesn't exist"}), 404
