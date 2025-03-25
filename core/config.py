import os
from re import T

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "FASTAPI RAG"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ACCESS_TOKEN_EXPIRE_DAY = 10
    MAIL_USERNAME: str=os.getenv("MAIL_FROM")
    MAIL_PASSWORD: str=os.getenv("MAIL_PASSWORD", "  ")
    MAIL_PORT: int=os.getenv("MAIL_PORT",587)
    MAIL_SERVER: str=os.getenv("MAIL_SERVER","smtp.gmail.com")
    MAIL_STARTTLS=os.getenv("MAIL_TLS",True)
    MAIL_SSL_TLS=os.getenv("MAIL_SSL",False)
    API_KEY_EXPIRY_DAYS: int=os.getenv("API_KEY_EXPIRY_DAYS",30)
    MONGODB_URL:str = os.getenv("mongo")
    GOOGLE_API_KEY:str = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY:str = os.getenv("GROQ_API_KEY")
    LANGCHAIN_API_KEY:str = os.getenv("LANGCHAIN_API_KEY")


settings = Settings()
