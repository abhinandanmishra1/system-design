from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from ..controllers import SocialMediaDB
users_router = APIRouter()
db = SocialMediaDB()

class RegionEnum(Enum):
    """Enum for region"""
    NA = "NA"
    ASIA = "ASIA"
    EU = "EU"
    OTHER = "OTHER"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    region: RegionEnum

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    region: str
    full_name: Optional[str]
    bio: Optional[str]
    profile_picture_url: Optional[str]

@users_router.get("/")
async def get_users():
    try:
        users = db.get_all_users()
        return {
            "users": [{"id": user[0], "username": user[1], "email": user[2], "region": user[6]} for user in users]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get users")

@users_router.post("/")
async def create_user(user: UserCreate):
    try:
        hashed_password = user.password  # You should hash the password
        user_id = db.create_user(user.username, user.email, hashed_password, user.region.value)
        return {"id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    try:
        user = db.get_user(user_id)
        return UserResponse(
            user_id=user[0],
            username=user[1],
            email=user[2],
            full_name=user[4],
            bio=user[5],
            region=user[6],
            profile_picture_url=user[7],
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@users_router.on_event("shutdown")
def shutdown_event():
    db.close()
