from fastapi import APIRouter, Depends, Path, HTTPException
from database import  SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from models import todosapp
from .auth import get_current_user





router=APIRouter(
    prefix="/admin",
    tags=['Admin endpoint']
)







def db_get():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()    



db_dependency=Annotated[Session, Depends(db_get)]
user_dependency=Annotated[dict, Depends(get_current_user)]

@router.get("/adminget")
async def readall(user:user_dependency, db: db_dependency):
    print(user.get('user_role'))
    if user is False or user.get('user_role')!='admin':
        raise HTTPException(status_code=404, detail='Authentication failed')
    todo_model=db.query(todosapp).all()
    return todo_model


#delete endpoint

@router.delete("/delete_todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_todo(user: user_dependency, db:db_dependency, todo_id:int=Path(gt=0)):
     if user is False or user.get("Role") != 'admin':
        raise HTTPException(status_code=404, detail='Authentication failed')
     
     
     todo_model=db.query(todosapp).filter(todosapp.ID==todo_id).first()
     if todo_model is None:
         raise HTTPException(status_code=404, detail='todo not found')
     db.query(todosapp).filter(todosapp.ID==todo_id).delete()
     db.commit()

