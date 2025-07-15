import sqlalchemy
from hobbyroom.settings import settings

postgres_db = sqlalchemy.create_engine(settings.db_url)
