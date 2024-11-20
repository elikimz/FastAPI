from jose import ExpiredSignatureError, JWSError,jwt
from datetime import datetime,timedelta
from app import schema
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')




SECRET_KEY="KIM"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1

def create_acess_token(data:dict):
  to_ecode=data.copy()

  expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_ecode.update({"exp":expire})

  

  encoded_jwt= jwt.encode(to_ecode,SECRET_KEY,algorithm=ALGORITHM)

  return encoded_jwt

def verify_access_token(token:str,credential_exemption):
  
    try:

          payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
          id:str=payload.get("user_id")
          if id is None:
           raise credential_exemption
          token_data=schema.TokenData(id=id)
    except ExpiredSignatureError:
        # Token has expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="session has expired, please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
          
    except JWSError :
       raise credential_exemption
    
    return token_data
    

def get_current_user(token:str=Depends(oauth2_scheme)):
   credential_exemption=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"www-Authenticate":"bearer"})
   return  verify_access_token(token,credential_exemption)


