from fastapi import APIRouter, Depends, Path, HTTPException
from database import  SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from models import todosapp, Users
from .auth import get_current_user,bcrpt_context





router=APIRouter(
    prefix="/user",
    tags=['Users endpoint']
)







def db_get():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()    



db_dependency=Annotated[Session, Depends(db_get)]
user_dependency=Annotated[dict, Depends(get_current_user)]




@router.get("/read_users")
async def read_all_user(user:user_dependency, db: db_dependency):
    if user is False:
        raise HTTPException(status_code=404, detail='Authentication Failed')
    todo_model=db.query(Users).filter(Users.ID==user.get('user_id')).first()
    return  todo_model



#basemodel

class verify_pass(BaseModel):
    password : str
    new_password: str=Path(min_length=5)




#change password 

@router.put("/change_password")
async def change_password(user:user_dependency, db:db_dependency, verify_pass: verify_pass, ):
    if user is False:
        raise HTTPException(status_code=404, detail='Authentication Failed')
    user_model=db.query(Users).filter(Users.ID==user.get('user_id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='todo not found')
    if not bcrpt_context.verify(verify_pass.password, user_model.Hashed_password):
        raise HTTPException(status_code=404, detail='wrong password')
    user_model.Hashed_password=bcrpt_context.hash(verify_pass.new_password)
 
    db.add(user_model)
    db.commit()


@router.put("/update_ph/{phone_number}")
async def update_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is False:
        raise HTTPException(status_code=404, detail='Authentication Failed')
    user_model=db.query(Users).filter(Users.ID==user.get('user_id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='todo not')
    user_model.phone_number=phone_number
    db.add(user_model)
    db.commit()


    
    
