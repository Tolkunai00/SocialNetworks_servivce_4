from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from stories_site.schemas.schema import (
    Stories, StoriesCreate,
    StoriesLike, StoriesLikeCreate,
    StoriesComment, StoriesCommentCreate, StoriesCommentUpdate
)

stories_router = APIRouter(prefix="/stories", tags=["Stories"])


@stories_router.get("/", response_model=List[Stories])
async def get_stories_list():
    return []


@stories_router.get("/{story_id}", response_model=Stories)
async def get_story_by_id(story_id: int):
    story = None
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="История не найдена")
    return story


@stories_router.post("/", response_model=Stories, status_code=status.HTTP_201_CREATED)
async def create_story(story_data: StoriesCreate):
    return story_data


@stories_router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(story_id: int):
    return None

@stories_router.get("/{story_id}/likes", response_model=List[StoriesLike])
async def get_story_likes(story_id: int):
    return []


@stories_router.post("/like", response_model=StoriesLike, status_code=status.HTTP_201_CREATED)
async def toggle_or_create_like(like_data: StoriesLikeCreate):
    return like_data


@stories_router.delete("/like/{like_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(like_id: int):
    return None


@stories_router.get("/{story_id}/comments", response_model=List[StoriesComment])
async def get_story_comments(story_id: int):
    return []


@stories_router.post("/comment", response_model=StoriesComment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: StoriesCommentCreate):
    return comment_data


@stories_router.patch("/comment/{comment_id}", response_model=StoriesComment)
async def update_comment(comment_id: int, update_data: StoriesCommentUpdate):
    if update_data.text is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поле text не должно быть пустым"
        )
    return update_data


@stories_router.delete("/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int):
    return None