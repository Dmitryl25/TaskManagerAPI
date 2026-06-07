from fastapi import APIRouter, status, Depends
from ..deps import get_db, get_current_user
from app.services.comment import CommentService
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Sequence

from uuid import UUID



router = APIRouter(tags=['comments'])

@router.post("/tasks/{task_id}/comments")
async def create_comment(task_id: UUID,
                         comment: CommentCreate,
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_user)):
    new_comment = await CommentService(db).create_comment(task_id=task_id,
                                                          auther_id=user.id,
                                                          data=comment)
    return CommentResponse.model_validate(new_comment)

@router.get("/tasks/{task_id}/comments")
async def get_task_comments(task_id: UUID,
                            db: AsyncSession = Depends(get_db),
                            user: User = Depends(get_current_user)):
    comments = await CommentService(db).get_task_comments(task_id=task_id,
                                                          user_id=user.id)
    return [CommentResponse.model_validate(comment) for comment in comments]


@router.patch("/comments/{comment_id}")
async def update_comments(comment_id: UUID,
                          data: CommentUpdate,
                          db: AsyncSession = Depends(get_db),
                          user: User = Depends(get_current_user)):
    comment_updated = await CommentService(db).update_comment(comment_id=comment_id,
                                                              data=data,
                                                              user_id=user.id)
    return CommentResponse.model_validate(comment_updated)

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: UUID,
                          db: AsyncSession = Depends(get_db),
                          user: User = Depends(get_current_user)):
    await CommentService(db).delete_comment(comment_id=comment_id,
                                            user_id=user.id)
