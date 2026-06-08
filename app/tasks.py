from .celery_app import celery_app
import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import delete, select
from app.core.config import settings
from app.models.token import Token
from app.models.task import Task

@celery_app.task
def send_welcome_email(email: str):
    print(f"Sending welcome email to {email}")

async def cleanup_revoked_tokens_async_function():
    engine = create_async_engine(settings.database.database_url)
    session = async_sessionmaker(bind=engine)
    async with session() as session:
        await session.execute(delete(Token)
                              .where(Token.revoked_at != None,
                                     Token.revoked_at < datetime.now(timezone.utc) - timedelta(days=30)))
        await session.commit()
    await engine.dispose()

async def check_deadline_tasks_async_function():
    engine = create_async_engine(settings.database.database_url)
    session = async_sessionmaker(bind=engine)
    async with session() as session:
        result = await session.execute(select(Task)
                                       .where(Task.status != "done",
                                              Task.due_date < datetime.now(timezone.utc) + timedelta(days=1)))
        tasks = result.scalars().all()
        for task in tasks:
            print(f"Task {task.title} deadline is tomorrow!")
    await engine.dispose()

@celery_app.task
def cleanup_revoked_tokens():
    asyncio.run(cleanup_revoked_tokens_async_function())

@celery_app.task
def check_deadline_tasks():
    asyncio.run(check_deadline_tasks_async_function())

