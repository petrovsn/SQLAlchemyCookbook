from sqlalchemy.ext.asyncio import create_async_engine
from alembic_src.configs import database_filename
from alembic_src.models import Base
from sqlalchemy import create_engine

async def redeclare_db_async(filename = database_filename, echo = True):
    engine = create_async_engine(f"sqlite+aiosqlite:///{filename}", echo=echo, future=True)
    #async with engine.begin() as conn:
    #    await conn.run_sync(Base.metadata.create_all)
    return engine

def redeclare_db(filename = database_filename, echo = True):
    engine = create_engine(f"sqlite+pysqlite:///{filename}", echo=echo, future=True)
    #Base.metadata.create_all(engine)
    return engine