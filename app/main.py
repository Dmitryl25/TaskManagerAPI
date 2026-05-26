import sqlalchemy
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .api.deps import get_db

app = FastAPI()


@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(text('SELECT 1'))
    return {"status": "ok"}
