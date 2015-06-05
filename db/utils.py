import contextlib
import functools
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(config.db_url, echo = False)
SessionClass = sessionmaker(bind = engine, expire_on_commit = False)


@contextlib.contextmanager
def get_temp_session():
    try:
        session = SessionClass()
        yield session
    finally:
        session.commit()
        session.close()


def ensure_session(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        session = kwargs.pop('session', None)
        if not session:
            with get_temp_session() as session:
                kwargs['session'] = session
                return f(*args, **kwargs)
        else:
            kwargs['session'] = session
            return f(*args, **kwargs)
    return wrapper
