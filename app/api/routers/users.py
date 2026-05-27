from fastapi import APIRouter, Depends, status, HTTPException
from ..deps import get_current_user
from app.schemas.user import UserResponse
from app.models.user import User


router = APIRouter(prefix="/users",
                   tags=["users"])

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)