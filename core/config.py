from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Project"
    debug: bool = True

    # Database Config
    db_host: str = "localhost"
    db_port: int = 3306
    db_database: str = "deep_scan"
    db_username: str = "root"
    db_password: str = ""

    # JWT Config
    algorithm: str = ""
    secret_key: str = ""
    expire: int = ""

    # timezone
    timezone: str = ""

    # Email Config
    mail_mailer: str = "smtp"
    mail_host: str = "smtp.gmail.com"
    mail_port: int = 587
    mail_username: str = ""
    mail_password: str = ""
    mail_encryption: str = "tls"
    mail_from_address: str = "no-reply@example.com"
    mail_from_name: str = "FastAPI Project"

    # upload file
    upload_dir: str = "public/uploads"
    allowed_content_types: str = "image/jpeg", "image/png", "application/pdf"
    max_file_size: int = 5 * 1024 * 1024

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"

    @property
    def mail_conf(self) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=self.mail_username,
            MAIL_PASSWORD=self.mail_password,
            MAIL_FROM=self.mail_from_address,
            MAIL_FROM_NAME=self.mail_from_name,
            MAIL_PORT=self.mail_port,
            MAIL_SERVER=self.mail_host,
            MAIL_TLS=self.mail_encryption.lower() == "tls",
            MAIL_SSL=self.mail_encryption.lower() == "ssl",
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

    @property
    def content_types(self):
        return self.allowed_content_types.split(",")

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
