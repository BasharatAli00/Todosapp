from fastapi import APIRouter, Depends, Path, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from models import todosapp
from .auth import get_current_user

# IMPORT THE NEW AI FUNCTIONS
from ai_services import add_todo_to_vector_store, delete_todo_from_vector_store, ask_ai_about_todos

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

## read all books get
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency ,db : db_dependency):
    if user is False:
        raise HTTPException(status_code=404, detail='Authentication Failed')
    return db.query(todosapp).filter(todosapp.Owner_id==user.get('user_id')).all()      

### path 
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_id(user: user_dependency, db : db_dependency, todo_id :int=Path(gt=0)):
    if user is False:
        raise HTTPException(status_code=404, detail='Authentication Failed')
    todo_model=db.query(todosapp).filter(todosapp.ID==todo_id).filter(todosapp.Owner_id==user.get('user_id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='item not found')  

# basemodel
class Todo_Request(BaseModel):
    Title : str = Field(min_length=3)
    Description: str = Field(min_length=3, max_length=100)
    Priority: int = Field(gt=0, lt=6)
    Complete: bool
    
### post
@router.post("/todocreate", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db : db_dependency, todo_request : Todo_Request):
    if user is False:
        raise HTTPException(status_code=404, detail="Unauthorized")
    
    todo_model=todosapp(**todo_request.model_dump(), Owner_id=user.get('user_id'))
    db.add(todo_model)
    db.commit()
    
    # REFRESH the model to get the auto-generated ID from the database
    db.refresh(todo_model)
    
    # ADD TO VECTOR STORE
    add_todo_to_vector_store(
        todo_id=todo_model.ID,
        title=todo_model.Title,
        description=todo_model.Description,
        owner_id=todo_model.Owner_id
    )

### update 
@router.put("/todo/update/{todo_id}")
async def update_todo(user:user_dependency,
                      db : db_dependency,
                       todo_request: Todo_Request,
                         todo_id:int=Path(gt=0)):
    if user is False:
        raise HTTPException(status_code=404, detail='Authorization Failed')
    
    todo_model=db.query(todosapp).filter(todosapp.ID==todo_id).filter(todosapp.Owner_id==user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo is not found')
    
    todo_model.Title=todo_request.Title
    todo_model.Description=todo_request.Description
    todo_model.Priority=todo_request.Priority
    todo_model.Complete=todo_request.Complete
    
    db.add(todo_model)
    db.commit()

    # UPDATE IN VECTOR STORE (ChromaDB replaces the existing vector if the ID matches)
    add_todo_to_vector_store(
        todo_id=todo_id,
        title=todo_model.Title,
        description=todo_model.Description,
        owner_id=user.get('user_id')
    )

#### delete endpoint 
@router.delete("/delete_todo/{todo_id}")
async def delete_todd(user: user_dependency, 
                      db: db_dependency,
                        todo_id: int=Path(gt=0)):
        
    if user is False:
       raise HTTPException(status_code=404, detail='Authorization Failed')
    
    todo_model=db.query(todosapp).filter(todosapp.ID==todo_id).filter(todosapp.Owner_id==user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')
    
    db.query(todosapp).filter(todosapp.ID==todo_id).filter(todosapp.Owner_id==user.get('user_id')).delete()
    db.commit()

    # REMOVE FROM VECTOR STORE
    delete_todo_from_vector_store(todo_id=todo_id)





# Add this new Pydantic model for the AI Chat request
class ChatRequest(BaseModel):
    query: str = Field(min_length=2)

# Add the new endpoint
@router.post("/chat", status_code=status.HTTP_200_OK)
async def chat_with_ai(user: user_dependency, chat_request: ChatRequest):
    """Endpoint for the frontend to ask questions about tasks."""
    if user is False:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    try:
        # Pass the query and the secure user_id to the LangChain service
        ai_response = ask_ai_about_todos(
            query=chat_request.query, 
            owner_id=user.get('user_id')
        )
        
        return {"response": ai_response}
        
    except Exception as e:
        print(f"AI Chat Error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong with the AI assistant.")