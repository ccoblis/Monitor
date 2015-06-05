from db import models
from db import utils
from uuid import uuid4
# from sqlalchemy import update


def create_tables():
    models.Base.metadata.create_all(utils.engine)


@utils.ensure_session
def add_data(id = None, data = None, session = None):
    if data is not None:
        needUpdate = None
        if id is None:
            id = uuid4().int >> 96  # 32 key length
        else:
            needUpdate = get_data_id(id)

        if needUpdate is None:
            info = models.Info(id = id, data = data)
            session.add(info)
        else:
            session.query(models.Info) \
                   .filter_by(id = id) \
                   .update({models.Info.data: data})
    else:
        raise Exception("data can't be None")

@utils.ensure_session
def get_data(session = None):
    query = session.query(models.Info)
    return query.order_by(models.Info.id).all()


@utils.ensure_session
def get_data_id(id = None, session = None):
    return session.query(models.Info).filter_by(id = id).first()