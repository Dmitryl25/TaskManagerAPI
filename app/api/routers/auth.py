from fastapi import APIRouter, Depends, status
from ..deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreated, UserResponse, Tokens, RefreshTokenRequest
from app.services.user import UserService
from app.core.security import create_access_token, create_refresh_token
from app.core.limiter import limiter
from fastapi import Request
from app.core.logger import logger

router = APIRouter(prefix="/auth",
                   tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreated,
                   db: AsyncSession = Depends(get_db)):
    user_register = await UserService(db).register(user)

    logger.info("user_registered", email=user.email)

    return UserResponse.model_validate(user_register)

@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def login(request: Request,
                user: UserCreated,
                db: AsyncSession = Depends(get_db)):
    user_login, token = await UserService(db).login(user)
    logger.info("user_logged_in", email=user.email)
    return Tokens(access_token=create_access_token(user_login.id),
                  refresh_token=token)

@router.post("/refresh")
async def refresh(token: RefreshTokenRequest,
                  db: AsyncSession = Depends(get_db)):
    access_token, refresh_token = await UserService(db).refresh(token.refresh_token)
    return Tokens(access_token=access_token,
                  refresh_token=refresh_token)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(token: RefreshTokenRequest,
                 db: AsyncSession = Depends(get_db)):
    await UserService(db).logout(token.refresh_token)
