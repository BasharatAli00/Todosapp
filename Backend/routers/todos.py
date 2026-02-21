from fastapi import APIRouter, Depends, Path, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from models import todosapp
from .auth import get_current_user

# Import the refined AI function
from ai_services import get_ai_response

router = APIRouter(
    prefix="/todos",
    tags=['Todos endpoint']
)

def db_get():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(db_get)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class Todo_Request(BaseModel):
    Title : str = Field(min_length=3)
    Description: str = Field(min_length=3, max_length=100)
    Priority: int = Field(gt=0, lt=6)
    Complete: bool

class ChatRequest(BaseModel):
    query: str = Field(min_length=2)

## --- STANDARD TODO ENDPOINTS ---

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency ,db : db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(todosapp).filter(todosapp.Owner_id==user.get('user_id')).all()      

@router.post("/todocreate", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db : db_dependency, todo_request : Todo_Request):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo_model=todosapp(**todo_request.model_dump(), Owner_id=user.get('user_id'))
    db.add(todo_model)
    db.commit()
    return {"status": "Created"}

@router.put("/todo/update/{todo_id}")
async def update_todo(user:user_dependency, db : db_dependency, todo_request: Todo_Request, todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authorization Failed')
    
    todo_model=db.query(todosapp).filter(todosapp.ID==todo_id).filter(todosapp.Owner_id==user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo is not found')
    
    todo_model.Title=todo_request.Title
    todo_model.Description=todo_request.Description
    todo_model.Priority=todo_request.Priority
    todo_model.Complete=todo_request.Complete
    
    db.add(todo_model)
    db.commit()
    return {"status": "Updated"}

@router.delete("/delete_todo/{todo_id}")
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int=Path(gt=0)):
    if user is None:
       raise HTTPException(status_code=401, detail='Authorization Failed')
    
    todo_model=db.query(todosapp).filter(todosapp.ID==todo_id).filter(todosapp.Owner_id==user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')
    
    db.query(todosapp).filter(todosapp.ID==todo_id).filter(todosapp.Owner_id==user.get('user_id')).delete()
    db.commit()
    return {"status": "Deleted"}

## --- NEW AI CHAT ENDPOINT ---

@router.post("/chat", status_code=status.HTTP_200_OK)
async def chat_with_ai(user: user_dependency, db: db_dependency, chat_request: ChatRequest):
    """Endpoint that fetches todos from DB and feeds them to the AI."""
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    try:
        # 1. Fetch all todos for this specific user from Supabase
        user_todos = db.query(todosapp).filter(todosapp.Owner_id == user.get('user_id')).all()
        
        # 2. Pass the user's query and their actual database tasks to the AI
        ai_response = get_ai_response(
            user_query=chat_request.query, 
            todos_from_db=user_todos
        )
        
        return {"response": ai_response}
        
    except Exception as e:
        print(f"AI Chat Error: {e}")
        raise HTTPException(status_code=500, detail="The AI assistant is having a nap. Try again later.")