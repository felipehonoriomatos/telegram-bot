from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Telegram
    telegram_token: str

    # Google Gemini
    gemini_api_key: str

    # Bot
    bot_name: str = "Assistente Virtual"
    bot_system_prompt: str = (
        "Você é um assistente virtual prestativo e educado. "
        "Responda sempre em português, de forma clara e objetiva. "
        "Seja cordial e profissional."
    )

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
