


from sqlalchemy import create_engine


engine = create_async_engine("postgresql+asyncpg://user:pass@localhost:5432/db",
                             echo=True, pool_size=10)