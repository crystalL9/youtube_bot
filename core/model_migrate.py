import pkgutil

import apps.models
from core.database import Base, engine, SessionLocal


def init_tables():
    for loader, module_name, is_pkg in pkgutil.walk_packages(path=apps.models.__path__,
                                                             prefix=apps.models.__name__ + '.'):
        __import__(module_name)
        print(module_name)

    Base.metadata.create_all(bind=engine)

def db_connect():
    db = SessionLocal()
    print("OL")
    init_tables()
    try:
        yield db
    finally:
        db.close()