# from tkinter.tix import STATUS
# from fastapi import HTTPException,Depends, Response
# from random import randrange
from fastapi import FastAPI
# from typing import Optional, Union,List
# from pydantic import BaseModel
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from app import model,schema,utils
from app.database import engine,get_db
# from  sqlalchemy.orm import Session
from app.routers import posts,users,auth







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





    
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


