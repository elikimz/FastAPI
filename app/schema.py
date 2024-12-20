import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional




class PostBase(BaseModel):
         title: str
         content: str
         published: bool=True
       

class PostCreate(PostBase):
      pass

class Response(PostBase):
         user_id:int
         created_at:datetime.datetime

         class Config:
                 orm_mode=True



class UserCreate(BaseModel):
        email:EmailStr
        password:str   

class UserOut(BaseModel):
        id:int
        email:EmailStr
        created_at:datetime.datetime
        updated_at:datetime.datetime
        class Config:
                 orm_mode=True

class UserLogin(BaseModel):
        email:EmailStr
        password:str

class Token(BaseModel):
        access_token:str
        token_type:str

class TokenData(BaseModel):
        id:Optional[int]=None