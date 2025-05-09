import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    # Application

    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
