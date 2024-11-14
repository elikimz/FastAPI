from random import randrange
from fastapi import FastAPI
from typing import Optional, Union
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    publish: bool=False
    rating:Optional[int]=None

from fastapi.params import Body
my_post=[{"title":"post 1", "content":"my new post","id":1}, {"title":"post 2", "content":"my new post","id":2}]


def my_index_delete(id):
   for i,p in  enumerate(my_post):
     if p["id"]==id:
        return i

     return -1
     




app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "Welcome to my API server using python"}


@app.get("/posts")
def read_posts():
    return{"Data":my_post}

@app.post("/posts")
def create_post(new_post:Post):
    my_dict=new_post.dict()
    my_dict["id"]=randrange(0,100)
    my_post.append(my_dict)
    print(my_dict)
    return {"message":my_dict}
    
@app.get("/posts/{id}")
def get_posts(id:int):
    print(id)
    return {"message":my_post(id)}

@app.delete("/post/{id}")
def delete_post(id: int):  # Add `id` as a parameter to the function
    index = my_index_delete(id)
    if index != -1:
        my_post.pop(index)
        return {"message": "Post deleted successfully"}
    else:
        return {"error": f"Post with id {id} not found"}