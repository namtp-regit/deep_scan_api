from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Project"
    debug: bool = True

    db_host: str = "localhost"
    db_port: int = 3306
    db_database: str = "deep_scan"
    db_username: str = "root"
    db_password: str = ""

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
