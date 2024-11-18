from tkinter.tix import STATUS
from fastapi import HTTPException,Depends, Response
from random import randrange
from fastapi import FastAPI
from typing import Optional, Union
from pydantic import BaseModel
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from app import model
from app.database import engine,get_db
from  sqlalchemy.orm import Session




model.Base.metadata.create_all(bind=engine)

app=FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool=False
    
    

while True :
         try:
              conn=psycopg2.connect(host='localhost',database='FastAPI',user='postgres',password='40284433'
    ,cursor_factory=RealDictCursor)
              cursor=conn.cursor()
              print("Database Connected Successifully")
              break
         except Exception as error:
          print("Database connection failed")
          print("Error:",error)
          time.sleep(2)




from fastapi.params import Body
my_post=[{"title":"post 1", "content":"my new post","id":1}, {"title":"post 2", "content":"my new post","id":2}]


def my_index_delete(id):
   for i,p in  enumerate(my_post):
     if p["id"]==id:
        return i

     return -1
 


@app.post("/posts")
def create_post(new_post:Post,db:Session=Depends(get_db)):
    # print(new_post.dict())
    new_post=model.Post(**new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{"data":new_post}


@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
      posts=db.query(model.Post).all()
    

      return {"message":posts}
   

    
@app.get("/posts/{id}")
def get_posts(id:int,db:Session=Depends(get_db)):
    posts=db.query(model.Post).filter(model.Post.id==id).first()
   
    if not posts:
      raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
     
    return {"message":posts}


@app.delete("/post/{id}")
def delete_post(id: int,db:Session=Depends(get_db)):  # Add `id` as a parameter to the function
     post=db.query(model.Post).filter(model.Post.id==id)
     

     if post.first()==None:
         raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
     post.delete(synchronize_session=False)
     db.commit()
     return{"message":"deleted successifully"}
        
        


@app.put("/posts/{id}") 
def update_post(id:int,updated_post_data: Post,db:Session=Depends(get_db)):
    updated_post=db.query(model.Post).filter(model.Post.id==id)
    updated=updated_post.first()
    if updated==None:
         raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
    updated_post.update(updated_post_data.dict(),synchronize_session=False)
    db.commit()


    return {"message": "Post updated successfully", "data": updated_post.first()}
