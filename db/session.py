from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Config

# Create an SQLAlchemy engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
