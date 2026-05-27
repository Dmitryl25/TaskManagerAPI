from fastapi import APIRouter, Depends, status
from ..deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreated, UserResponse
from app.services.user import UserService


router = APIRouter(prefix="/auth",
                   tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreated,
                   db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user_register = await user_service.register(user)
    return UserResponse.model_validate(user_register)
