from fastapi import FastAPI
from .routes import posts_router, sharded_posts_router, vertical_posts_router, users_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(sharded_posts_router, prefix="/sharded_posts", tags=["sharded_posts"])
app.include_router(vertical_posts_router, prefix="/vertical_posts", tags=["vertical_posts"])
app.include_router(users_router, prefix="/users", tags=["users"])
