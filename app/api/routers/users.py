from fastapi import APIRouter, Depends, status, HTTPException
from ..deps import get_current_user, get_db
from app.schemas.user import UserResponse, UserUpdate
from app.models.user import User
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService

router = APIRouter(prefix="/users",
                   tags=["users"])

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)

@router.patch("/me")
async def update_user(data: UserUpdate,
                      db: AsyncSession = Depends(get_db),
                      user: User = Depends(get_current_user)):
    user_updated = await UserService(db).update_user(user_id=user.id,
                                                     data=data)
    return UserResponse.model_validate(user_updated)