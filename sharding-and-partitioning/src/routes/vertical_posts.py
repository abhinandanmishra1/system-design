from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..controllers import VerticalPartitionedDB
vertical_posts_router = APIRouter()

vertical_db = VerticalPartitionedDB()

class PostCreate(BaseModel):
    user_id: int
    content: str
    media_url: Optional[str]

class PostResponse(BaseModel):
    post_id: int
    user_id: int
    content: str
    created_at: str
    media_url: Optional[str]
    media_type: Optional[str]
    likes_count: int
    shares_count: int
    comments_count: int
    views_count: int

@vertical_posts_router.post("/", response_model=PostResponse)
async def create_vertical_post(post: PostCreate):
    try:
        post_id = vertical_db.create_post(post.user_id, post.content)
        created_post = vertical_db.get_post_complete(post_id)
        return PostResponse(
            post_id=created_post[0],
            user_id=created_post[1],
            content=created_post[2],
            created_at=str(created_post[3]),
            likes_count=created_post[6],
            comments_count=created_post[7]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@vertical_posts_router.get("/{post_id}", response_model=PostResponse)
async def get_vertical_post(post_id: int):
    try:
        post = vertical_db.get_post_complete(post_id)
        print(post)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return PostResponse(
            post_id=post[0],
            user_id=post[1],
            content=post[2],
            created_at=str(post[3]),
            media_url=post[4],
            media_type=post[5],
            likes_count=post[6],
            comments_count=post[7],
            shares_count=post[8],
            views_count=post[9]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@vertical_posts_router.on_event("shutdown")
def shutdown_event():
    vertical_db.close()
    