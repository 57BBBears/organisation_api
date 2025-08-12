from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env", extra="ignore")


class DatabaseConfig(CustomBaseSettings):
    driver: str = "postgresql+asyncpg"
    host: str = "localhost"
    db: str
    user: str
    password: str
    port: int = 5432

    model_config = SettingsConfigDict(env_prefix="DATABASE_")


class SeedConfig(CustomBaseSettings):
    organisation_num: int = 50
    building_num: int = 20

    model_config = SettingsConfigDict(env_prefix="SEED_")


class Config(CustomBaseSettings):
    database: DatabaseConfig = DatabaseConfig()
    api_secret_key: str
    min_radius: int = 0
    seed: SeedConfig = SeedConfig()

    @property
    def database_url(self) -> str:
        return (
            f"{self.database.driver}://{self.database.user}:{self.database.password}"
            f"@{self.database.host}:{self.database.port}/{self.database.db}"
        )


config = Config()
