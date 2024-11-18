from tkinter.tix import STATUS
from fastapi import HTTPException,Depends, Response
from random import randrange
from fastapi import FastAPI
from typing import Optional, Union,List
from pydantic import BaseModel
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from app import model,schema
from app.database import engine,get_db
from  sqlalchemy.orm import Session
from passlib.context import CryptContext


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")




model.Base.metadata.create_all(bind=engine)

app=FastAPI()




    
    

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
 


@app.post("/posts",response_model=schema.Response)
def create_post(new_post:schema.PostCreate,db:Session=Depends(get_db)):
    # print(new_post.dict())
    new_post=model.Post(**new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/sqlalchemy",response_model=list[schema.Response])
def test_posts(db:Session=Depends(get_db)):
      posts=db.query(model.Post).all()
    

      return posts
   

    
@app.get("/posts/{id}",response_model=schema.Response)
def get_posts(id:int,db:Session=Depends(get_db)):
    posts=db.query(model.Post).filter(model.Post.id==id).first()
   
    if not posts:
      raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
     
    return posts


@app.delete("/post/{id}")
def delete_post(id: int,db:Session=Depends(get_db)):  # Add `id` as a parameter to the function
     post=db.query(model.Post).filter(model.Post.id==id)
     

     if post.first()==None:
         raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
     post.delete(synchronize_session=False)
     db.commit()
     return "deleted successifully"
        
        


@app.put("/posts/{id}",response_model=schema.Response) 
def update_post(id:int,updated_post_data:schema.PostBase,db:Session=Depends(get_db)):
    updated_post=db.query(model.Post).filter(model.Post.id==id)
    updated=updated_post.first()
    if updated==None:
         raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
    updated_post.update(updated_post_data.dict(),synchronize_session=False)
    db.commit()


    return updated_post.first()


@app.post("/users",response_model=schema.UserOut)
def create_user(user:schema.UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(model.User).filter(model.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password=pwd_context.hash(user.password)
    user.password=hashed_password


    new_user=model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user