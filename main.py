from fastapi import FastAPI
from typing import Optional, Union
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    publish: bool=False
    rating:Optional[int]=None

from fastapi.params import Body

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "Welcome to my API server using python"}
@app.get("/posts")
def read_posts():
    return [{"title": "Post 1", "content": "This is the first post"}, {"title": "Post 2", "content": "This is the second post"}]

@app.post("/createpost")
def create_post(new_post:Post):
    print(new_post.rating)
    return {"message": "Post created successfully"}