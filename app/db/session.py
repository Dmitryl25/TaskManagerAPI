from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from ..core.config import settings

engine = create_async_engine(settings.database.database_url)

AsyncSessionLocal = async_sessionmaker(bind=engine,
                                       autocommit=False,
                                       autoflush=False,
                                       expire_on_commit=False)
