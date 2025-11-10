from pydantic import BaseModel, field_validator, model_validator
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    postgres_host: str = os.getenv('POSTGRES_HOST', 'localhost')
    postgres_port: int = int(os.getenv('POSTGRES_PORT', 5433))
    postgres_db: str = os.getenv('POSTGRES_DB', 'indicadores_financieros')
    postgres_user: str = os.getenv('POSTGRES_USER') or ''
    postgres_password: str = os.getenv('POSTGRES_PASSWORD') or ''

    api_prefix: str = os.getenv('API_PREFIX', '/api')

    allowed_origins: List[str] = []
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')

    @field_validator('allowed_origins', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, list):
            return v
        env_val = os.getenv('ALLOWED_ORIGINS', '')
        if not env_val:
            return []
        return [item.strip() for item in env_val.split(',') if item.strip()]

    @model_validator(mode='after')
    def ensure_db_secrets(self):
        if not self.postgres_user or not self.postgres_password:
            raise ValueError("Missing required database credentials: POSTGRES_USER/POSTGRES_PASSWORD")
        return self


settings = Settings()
