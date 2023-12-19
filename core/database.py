import importlib.util
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.settings import settings

DATABASE_URL = settings.MYSQL_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DatabaseSetup:
    @staticmethod
    def init_models(directory_path):
        for filename in os.listdir(directory_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]  # Removing '.py' extension
                module_path = os.path.join(directory_path, filename)

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                globals()[module_name] = module
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def get_db():
        return SessionLocal()


db = SessionLocal()
