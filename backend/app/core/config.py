from uuid import UUID

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_service_key: str
    anthropic_api_key: str = ""
    claude_model: str = "claude-haiku-4-5-20251001"
    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-luna"
    environment: str = "production"
    dev_auth_bypass: bool = False
    dev_user_id: str | None = None

    @field_validator("dev_user_id", mode="before")
    @classmethod
    def normalize_dev_user_id(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized_value = str(value).strip()
        if not normalized_value:
            return None

        UUID(normalized_value)
        return normalized_value

    class Config:
        env_file = ".env"


settings = Settings()


def validate_dev_auth_settings() -> None:
    if not settings.dev_auth_bypass:
        return

    if settings.environment != "development":
        raise RuntimeError(
            "DEV_AUTH_BYPASS=true is only allowed when ENVIRONMENT=development"
        )

    if not settings.dev_user_id:
        raise RuntimeError(
            "DEV_USER_ID is required when DEV_AUTH_BYPASS=true. "
            "Set it to the UUID of an existing Supabase auth.users user."
        )

    try:
        UUID(settings.dev_user_id)
    except ValueError as error:
        raise RuntimeError(
            f"DEV_USER_ID must be a valid UUID, got {settings.dev_user_id!r}"
        ) from error
