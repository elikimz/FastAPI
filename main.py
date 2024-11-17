from fastapi import HTTPException,Depends
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
    publish: bool=False
    rating:Optional[int]=None
    

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
 




app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "Welcome to my API server using python"}


@app.get("/posts")
def read_posts():
    cursor.execute("""SELECT*FROM posts""")
    posts=cursor.fetchall()
    # print(posts)
    return{"Data":posts}

@app.post("/posts")
def create_post(new_post:Post,db:Session=Depends(get_db)):
    new_post=model.Post(title=new_post.title, content=new_post.content, published=new_post.publish)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{"data":new_post}
    # cursor.execute(
    #     """INSERT INTO posts(title,content) values (%s,%s)RETURNING*""",
    # (new_post.title,new_post.content)
    # )
    # latest_post=cursor.fetchone()
    # conn.commit()
    # # print(latest_post)
    # return {"message":latest_post}


    
@app.get("/posts/{id}")
def get_posts(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    latest=cursor.fetchone()
    # print(latest)
    if not latest:
      raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
     
    return {"message":latest}

@app.delete("/post/{id}")
def delete_post(id: int):  # Add `id` as a parameter to the function
      cursor.execute("""DELETE FROM posts WHERE id=%sRETURNING*""",(str(id),))
      deleted_post=cursor.fetchone()
      conn.commit()
      if not deleted_post:
         raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
        
      return {"message":deleted_post}

@app.put("/posts/{id}") 
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s  WHERE id=%sRETURNING*""",(post.title,post.content,str(id),))
    updated_post=cursor.fetchone()  
    conn.commit()
    if not updated_post:
         raise HTTPException(status_code=404,detail= f"post with id {id} is not found")


    return {"message":updated_post}

@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
      posts=db.query(model.Post).all()
    

      return {"message":posts}