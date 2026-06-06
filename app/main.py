import sqlalchemy
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .api.deps import get_db
from .api.routers.user import router as user_router
from .api.routers.users import router as users_router
from .api.routers.workspace import router as workspace_router
from .api.routers.project import router as project_router
from .api.routers.task import router as task_router

app = FastAPI()

app.include_router(user_router)
app.include_router(users_router)
app.include_router(workspace_router)
app.include_router(project_router)
app.include_router(task_router)


@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(text('SELECT 1'))
    return {"status": "ok"}
