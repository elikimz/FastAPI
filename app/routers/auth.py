from fastapi import APIRouter,Depends,status,HTTPException,Response
from pydantic import BaseModel
from sqlalchemy.orm import session
from..import database,schema,model,utils
from ..routers import auth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(tags=["Authentication"])

router=APIRouter(
    prefix="/login",
    tags=["LOGIN"]
)


class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/",response_model=Token)
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:session=Depends(database.get_db)):
   user= db.query(model.User).filter(model.User.email==user_credential.username).first()
   if not  user:
        raise HTTPException(status_code=404, detail="invalid credentials!")
   
   if not utils.verify(user_credential.password,user.password):

    raise HTTPException(status_code=404, detail="invalid credentials!")
   
   access_token=auth2.create_acess_token(data={"user_id":user.id})
   
   
   return {"access_token":access_token,"token_type":"bearer"}


   