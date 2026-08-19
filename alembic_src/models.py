from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import select, update, delete

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
# Твой код с моделями и engine = create_engine(...) должен быть выше
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Проверяем, что мы работаем именно с SQLite
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

@as_declarative() 
class Base(AsyncAttrs): 
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)

    def to_dict(self):
        """
        Преобразует объект модели в словарь.
        Возвращает все колонки таблицы.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def  __repr__(self):
        return str(self.to_dict())

class User(Base): 
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(nullable=True)
    posts = relationship("Post", back_populates="user") 
    tg_link: Mapped[str] = mapped_column(nullable=False)
    slogan: Mapped[str] = mapped_column(nullable=False, server_default="Per stradania to Sterne") 
 

class Post(Base): 
    __tablename__ = "posts"
    text = Column(String) 
    user_id = Column(Integer, ForeignKey("users.id")) 
    user = relationship("User", back_populates="posts") 

