import json

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.config.secrets import ENV

# fmt: off

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=ENV.get("POSTGRES_USER"),
    password=ENV.get("POSTGRES_PASSWORD"),
    host=ENV.get("POSTGRES_HOST"),
    port=ENV.get("POSTGRES_PORT"),
    database=ENV.get("POSTGRES_DB"),
)

DATABASE_PARAMS = {
    "pool_pre_ping": True,
    "echo": False,
    "pool_size": 10,
    "max_overflow": 50,
}

engine = create_engine(
    DATABASE_URL,
    **DATABASE_PARAMS,
    json_serializer=json.dumps,
    json_deserializer=json.loads,
)
DBSession = sessionmaker(bind=engine)
