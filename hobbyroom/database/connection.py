import sqlalchemy
from settings import settings

postgres_db = sqlalchemy.create_engine(settings.db_url)
