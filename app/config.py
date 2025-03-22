import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    # Application

    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
