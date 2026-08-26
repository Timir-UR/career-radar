

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

convention = {
    "ix": "ix_%(column_0_label)s",  # Индекс
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # Уникальное ограничение
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # Проверочное ограничение
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Внешний ключ
    "pk": "pk_%(table_name)s"  # Первичный ключ
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    metadata = metadata