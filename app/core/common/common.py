import sqlalchemy
from sqlalchemy.dialects.postgresql import insert

from app.extensions.database import db
from app.lib.exceptions.schema_validation import ValidatorException


def get_current_user():
    return "SYSTEM"


def save_bulk(data):
    db.session.add_all(data)
    db.session.commit()
    return data


def update_or_create(model, data, constraint):
    try:
        created = True
        filter_dict = {constraint[0]: data.get(constraint[0])}
        data_model = model.query.filter_by(**filter_dict).first()
        if data_model:
            created = False
        insert_stmt = insert(model).values(data)
        insert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=constraint, set_=data
        ).returning(model)
        result = db.session.execute(insert_stmt)
        return dict(result.fetchone()), db.session, created
    except sqlalchemy.exc.IntegrityError as e:
        db.session.expire_on_commit = False
        raise ValidatorException(
            "{}: '{}', {}".format(
                ",".join(constraint),
                data[constraint[0]],
                e.args[0].split("DETAIL: ")[-1].strip().replace('"', "'"),
            )
        )


def save_data(data):
    db.session.add(data)
    db.session.commit()
    return data
