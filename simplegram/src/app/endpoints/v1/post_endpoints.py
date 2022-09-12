import uuid
from typing import List
from fastapi import Depends
from fastapi.routing import APIRouter

from app.dependencies.auth import get_current_user
from app.dependencies.services import post_service
from app.schemas.post_schemas import (
    PostAction,
    PostAnalyticsRequestSchema,
    PostAnalyticsResponseSchema,
    PostEditRequestSchema,
    PostResponseSchema,
)
from app.schemas.user_schemas import UserRecordSchema
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags={"posts"})


@router.get("/analytics", response_model=List[PostAnalyticsResponseSchema])
async def get_analytics(
    body: PostAnalyticsRequestSchema, post_service: PostService = Depends(post_service)
):
    post_analytics = await post_service.get_analytics(body)
    return post_analytics


@router.post("/", response_model=PostResponseSchema)
async def create_post(
    body: PostEditRequestSchema,
    auth_user: UserRecordSchema = Depends(get_current_user),
    post_service: PostService = Depends(post_service),
) -> PostResponseSchema:
    return await post_service.create(auth_user, body)


@router.get("/", response_model=List[PostResponseSchema])
async def list_posts(
    post_service: PostService = Depends(post_service),
) -> List[PostResponseSchema]:
    return await post_service.list()


@router.get("/{post_id}", response_model=PostResponseSchema)
async def get_post(
    post_id: uuid.UUID,
    post_service: PostService = Depends(post_service),
) -> PostResponseSchema:
    return await post_service.get(post_id)


@router.post("/{post_id}/{post_action}", response_model=PostResponseSchema)
async def make_post_action(
    post_id: uuid.UUID,
    post_action: PostAction,
    auth_user: UserRecordSchema = Depends(get_current_user),
    post_service: PostService = Depends(post_service),
) -> PostResponseSchema:
    await post_service.make_action(post_id, post_action, auth_user)
    return await post_service.get(post_id)
