

from app import model,schema,utils
from app.database import engine,get_db
from  sqlalchemy.orm import Session
from fastapi import HTTPException,Depends, Response,APIRouter
from ..routers import auth2


router=APIRouter(
    prefix="/posts",
    tags=["POSTS"]
)


@router.post("",response_model=schema.Response)
def create_post(new_post:schema.PostCreate,db:Session=Depends(get_db),user_id:int=Depends(auth2.get_current_user)):
    # print(new_post.dict())
    new_post=model.Post(**new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("",response_model=list[schema.Response])
def test_posts(db:Session=Depends(get_db),user_id:int=Depends(auth2.get_current_user)):
      posts=db.query(model.Post).all()
    

      return posts
   

    
@router.get("/{id}",response_model=schema.Response)
def get_posts(id:int,db:Session=Depends(get_db),user_id:int=Depends(auth2.get_current_user)):
    posts=db.query(model.Post).filter(model.Post.id==id).first()
   
    if not posts:
      raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
     
    return posts


@router.delete("/{id}")
def delete_post(id: int,db:Session=Depends(get_db),user_id:int=Depends(auth2.get_current_user)):  # Add `id` as a parameter to the function
     post=db.query(model.Post).filter(model.Post.id==id)
     

     if post.first()==None:
         raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
     post.delete(synchronize_session=False)
     db.commit()
     return "deleted successifully"
        
        


@router.put("/{id}",response_model=schema.Response) 
def update_post(id:int,updated_post_data:schema.PostBase,db:Session=Depends(get_db),user_id:int=Depends(auth2.get_current_user)):
    updated_post=db.query(model.Post).filter(model.Post.id==id)
    updated=updated_post.first()
    if updated==None:
         raise HTTPException(status_code=404,detail= f"post with id {id} is not found")
    updated_post.update(updated_post_data.dict(),synchronize_session=False)
    db.commit()


    return updated_post.first()
