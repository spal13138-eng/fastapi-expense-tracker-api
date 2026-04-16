from sqlalchemy.orm import Session
from app import utils,schemas,models
from datetime import timedelta,datetime
from pydantic import BaseModel
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError,jwt
from fastapi import HTTPException,status,Depends
from app.config import settings

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINITES=settings.access_token_expire_minutes

oauth_scheme=OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINITES)
    
    to_encode.update({"exp":expire})

    encode=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encode

def verify_access_token(token:str,credentials_Exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id:int=payload.get("user_id")
        
        if id is None:
            raise credentials_Exception
        
        token_data=schemas.Token_data(id=id)

    except JWTError as e:
        raise credentials_Exception 

    return token_data 


def get_current_user(token:str=Depends(oauth_scheme),db:Session=Depends(get_db)):

    credentials_Exception=HTTPException(
       status_code=status.HTTP_401_UNAUTHORIZED,
       detail="Could not validate Credentials",
       headers={"WWW-Authenticate":"Bearer"}
    )

    token_data=verify_access_token(token,credentials_Exception)


    user=db.query(models.User).filter(models.User.id==token_data.id).first()

    if user is None:
        raise credentials_Exception
    
    return user
