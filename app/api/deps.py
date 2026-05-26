from ..db.session import AsyncSessionLocal

# Получение сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

