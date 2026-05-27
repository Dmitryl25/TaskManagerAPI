from ..db.session import AsyncSessionLocal
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from ..core.security import decode_token
from fastapi import status, HTTPException
from ..models.user import User
from ..services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


http_bearer = HTTPBearer()


# получение сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# получение пользователя по access-токену
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                           db: AsyncSession = Depends(get_db)) -> User:
    token = credentials.credentials
    decode = decode_token(token)
    if not decode:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    user = await UserService(db).get_user_by_id(UUID(decode["sub"]))

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return user

