import contextlib
import functools
import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Config = ConfigParser.ConfigParser()
Config.read("config.txt")
db_url = Config.get('DB', 'db_url')
engine = create_engine(db_url, echo = False)
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
