from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix  = "/users",
    tags = ["users"]

)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserConfirmation)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #Hash the password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())

    #Adding the instance of the class/relation Post to the db within the relation Post
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model= schemas.UserConfirmation)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id== id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user