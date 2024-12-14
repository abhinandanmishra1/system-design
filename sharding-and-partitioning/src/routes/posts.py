from fastapi import  HTTPException, APIRouter
from pydantic import BaseModel
from ..controllers import SocialMediaDB
posts_router = APIRouter()

db = SocialMediaDB()

class PostCreate(BaseModel):
    user_id: int
    content: str

class PostResponse(BaseModel):
    post_id: int
    user_id: int
    content: str

@posts_router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate):
    try:
        post_id = db.create_post(post.user_id, post.content)
        created_post = db.get_post(post_id)
        return PostResponse(
            post_id=created_post[0],
            user_id=created_post[1],
            content=created_post[2],
        )      
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@posts_router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    try:
        post = db.get_post(post_id)
        return PostResponse(
            post_id=post[0],
            user_id=post[1],
            content=post[2],
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@posts_router.on_event("shutdown")
def shutdown_event():
    db.close()
