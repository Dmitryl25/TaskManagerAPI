from fastapi import APIRouter, Depends, status
from ..deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreated, UserResponse, Tokens
from app.services.user import UserService
from app.core.security import create_access_token, create_refresh_token


router = APIRouter(prefix="/auth",
                   tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreated,
                   db: AsyncSession = Depends(get_db)):
    user_register = await UserService(db).register(user)
    return UserResponse.model_validate(user_register)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserCreated,
                db: AsyncSession = Depends(get_db)):
    user_login = await UserService(db).login(user)
    return Tokens(access_token=create_access_token(user_login.id),
                  refresh_token=create_refresh_token(user_login.id))
