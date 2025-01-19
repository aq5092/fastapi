from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict
app = FastAPI()

@app.get("/")
async def home() -> dict[str, str]:
    return {"Hello": "World", "test": "test"}


class User(BaseModel):
    id: int
    name: str
    email: str

users = [
    {"id": 1, "name": "Ahadbek", "email": "ahadjon.qodirov@uzautomotors.com"},
    {"id": 2, "name": "Elyorbek", "email": "elyorbek.nurmatov@uzautomotors.com"},
    {"id": 3, "name": "Furkatjon", "email": "furkatjon.toshmatov@uzautomotors.com"},
]

# @app.get("/contact")
# async def contact() -> int:
#     return 7777

class Post(BaseModel):
    id: int
    title: str
    content: str

# @app.get("/posts")
# async def posts() -> List[Post]:
#     return [
#         Post(title="First Post", content="This is the first post"),
#         Post(title="Second Post", content="This is the second post")
#     ]

posts = [
    {"id":1,"title": "Post 1", "content": "This is the content of post 1"},
    {"id":2,"title": "Post 2", "content": "This is the content of post 2"},
    {"id":3,"title": "Post 3", "content": "This is the content of post 3"},
]

# 1- variant
@app.get("/posts")
async def posts() -> List[Post]:
    post_obj = []
    for post in posts:
        post_obj.append(Post(id=post["id"], title=post["title"], content=post["content"])) 
    return post_obj

# 2- variant    
# @app.get("/posts")
# async def posts()-> List[Post]:
#     return [Post(**post) for post in posts]

#@app.delete("/posts/{post_id}")
# @app.get("/posts")
# async def get_posts() -> list:
#     return posts

# @app.get("/posts/{post_id}")
# async def get_post(post_id: int) -> dict:
#     for post in posts:
#         if post["id"] == post_id:
#             return post
#     return {"error": "Post not found"}

# @app.get("/search")
# async def search(post_id: Optional[int] = None) -> dict:
#     if post_id:
#         for post in posts:
#             if post["id"] == post_id:
#                 return post
#         return {"error": "Post not found"}
#     return posts
