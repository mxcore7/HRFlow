from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import get_db_url, load_config

Base = declarative_base()

_config = load_config()
engine = create_engine(get_db_url(_config), echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
