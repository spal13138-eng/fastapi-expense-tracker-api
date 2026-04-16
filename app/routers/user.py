from fastapi import FastAPI,HTTPException,Depends,status,APIRouter
from app.database import get_db
from app import schemas,models
from sqlalchemy.orm import Session
from app import utils

router=APIRouter(
    prefix="/signup",
    tags=["Register"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def registerUser(user:schemas.UserRegister,db:Session=Depends(get_db)):

    hashed_password=utils.hash(user.password)
    new_user=models.User(
        email=user.email,
        password=hashed_password
)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schemas.UserOut)
def getUser(id:int,db:Session=Depends(get_db)):

    user=db.query(models.User).filter(models.User.id==id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} is not found")
    
    return user