from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN_KEY: str
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_EXP_MINUTE: int = 5
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
