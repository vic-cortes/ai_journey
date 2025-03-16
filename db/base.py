# Import all the models, so that Base has them before being imported by Alembic
from app.models.user import User  # noqa
from db.base_class import Base

__all__ = ["Base", "User"]
