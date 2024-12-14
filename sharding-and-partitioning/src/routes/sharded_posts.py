from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..controllers import ShardedDB
from enum import Enum
sharded_posts_router = APIRouter()

sharded_db = ShardedDB()

# Mapping from post_id to shard_id stored in cache ( we can use redis for this)
# This will not be required actually
post_id_to_shard_id = {}

class ShardingStrategy(Enum):
    GEOGRAPHIC = "GEOGRAPHIC"
    RANGE = "RANGE"
    HASH = "HASH"

class ShardedPostCreate(BaseModel):
    user_id: int
    content: str
    sharding_strategy: ShardingStrategy

class PostResponse(BaseModel):
    post_id: int
    user_id: int
    content: str
    created_at: str
    shard_id: str

@sharded_posts_router.post("/", response_model=PostResponse)
async def create_sharded_post(post: ShardedPostCreate):
    try:
        response = sharded_db.create_post(post.sharding_strategy.value, post.user_id, post.content)
        post_id_to_shard_id[response["post_id"]] = response["shard_id"]
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@sharded_posts_router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    try:
        shard_id = post_id_to_shard_id[post_id]
        post = sharded_db.get_post(post_id, shard_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sharded_posts_router.on_event("shutdown")
def shutdown_event():
    sharded_db.close()
