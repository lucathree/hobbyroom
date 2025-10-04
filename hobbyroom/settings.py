import pendulum
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_url: str

    redis_host: str
    redis_port: int
    redis_password: str
    redis_db: int = 0

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def jwt_expiration_timedelta(self) -> pendulum.Duration:
        return pendulum.Duration(minutes=self.jwt_expiration_minutes)

    @property
    def redis_url(self) -> str:
        return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"


settings = Settings()
