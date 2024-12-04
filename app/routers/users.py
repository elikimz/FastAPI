from app import model,schema,utils
from app.database import engine,get_db
from  sqlalchemy.orm import Session
from fastapi import HTTPException,Depends, Response,APIRouter
from ..routers import auth2


router=APIRouter(
    prefix="/users",
    tags=["USERS"]
)


@router.post("",response_model=schema.UserOut)
def create_user(user:schema.UserCreate,db:Session=Depends(get_db),):
    existing_user = db.query(model.User).filter(model.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password=utils.pwd_context.hash(user.password)
    user.password=hashed_password


    new_user=model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schema.UserOut)
def get_user(id:int,db:Session=Depends(get_db),user_id:int=Depends(auth2.get_current_user)):
    user=db.query(model.User).filter(model.User.id==id).first()
    if user==None:
         raise HTTPException(status_code=404,detail= f"user with id {id} is not found")
    return user
