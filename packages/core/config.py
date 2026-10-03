"""Application settings and environment configuration for Cofunder."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global configuration settings for Cofunder services."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = Field(default="development", description="Runtime environment")
    log_level: str = Field(default="INFO", description="Log output level")
    secret_key: str = Field(default="dev-secret-key-at-least-32-characters-long", description="Secret key")

    database_url: str = Field(
        default="postgresql+psycopg://cofunder:cofunder@localhost:5432/cofunder",
        description="Async PostgreSQL connection URL",
    )
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )

    # Auth
    clerk_secret_key: str = Field(default="", description="Clerk secret key")
    clerk_jwks_url: str = Field(default="", description="Clerk JWKS public key endpoint")

    # LLM & Decision Layer
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    jev_api_key: str = Field(default="", description="TypeSafe Jev API key")
    jev_api_base: str = Field(default="https://api.typesafe.ai/v1", description="Jev API base URL")

    # Observability
    langsmith_api_key: str = Field(default="", description="LangSmith API key")
    langsmith_project: str = Field(default="cofunder-dev", description="LangSmith project name")
    langsmith_tracing: bool = Field(default=True, description="Enable LangSmith tracing")

    # AWS
    aws_region: str = Field(default="ap-south-1", description="Primary AWS region")
    aws_kms_key_id: str = Field(default="", description="AWS KMS key ID for token encryption")
    s3_sites_sandbox_bucket: str = Field(default="cofunder-sites-sandbox", description="S3 bucket for sandboxed landing pages")


def get_settings() -> Settings:
    """Retrieve validated application settings instance.

    Returns:
        Settings: The validated application configuration instance.
    """
    return Settings()
