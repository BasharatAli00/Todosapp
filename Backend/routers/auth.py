from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from jose import jwt, JWTError


#route
router=APIRouter(
     prefix='/auth',
     tags=['Authentication']
)


#db_dependency

def db_get():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()    



db_dependency=Annotated[Session, Depends(db_get)]


bcrpt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2bearer=OAuth2PasswordBearer(tokenUrl='/auth/token')
SECRET_KEY='N33l4w-lB2xYvP2N9jB-2u3e6zC5mK0g9dE0s-Z-X5c'
ALGO='HS256'





#JWTencoder

def create_access_token(username :str, user_id: int, Role:str, expires_date : timedelta):
    encode={'sub':username, 'user_id':user_id, 'user_role':Role}
    expires=datetime.now(timezone.utc)+expires_date
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGO)



##JWTDecoder

async def get_current_user(token: Annotated[str, Depends(oauth2bearer)]):
    try:
        paylaod=jwt.decode(token, SECRET_KEY, algorithms=ALGO)
        username:str=paylaod.get('sub')
        user_id:int=paylaod.get('user_id')
        user_role: str=paylaod.get('user_role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
        return {"username": username, "user_id": user_id, 'user_role': user_role}
    except JWTError:
                
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')




#authenticate method

def user_authenticate(username:str, password:str, db: db_dependency):
    user=db.query(Users).filter(Users.Username==username).first()
    if not user:
        return  False
    

    if not bcrpt_context.verify(password, user.Hashed_password):
        return  False
    
    
    return user



###basemodel

class Create_user_request(BaseModel):
    Email: str
    Username : str
    First_name :str 
    Last_name : str
    Password : str
    Is_active : bool
    Role : str
    phone_number: str


class Token(BaseModel):
    access_token : str
    access_type : str
    



@router.post("/user_auth", status_code=status.HTTP_201_CREATED)
async def create_userl(create_book_request: Create_user_request, db: db_dependency):
    # ✅ Check username
    existing_user = db.query(Users).filter(Users.Username == create_book_request.Username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # ✅ Check email
    existing_email = db.query(Users).filter(Users.Email == create_book_request.Email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # ✅ Create user
    create_user_model = Users(
        Email=create_book_request.Email,
        Username=create_book_request.Username,
        First_name=create_book_request.First_name,
        Last_name=create_book_request.Last_name,
        Hashed_password=bcrpt_context.hash(create_book_request.Password),
        Is_active=create_book_request.Is_active,
        Role=create_book_request.Role,
        phone_number=create_book_request.phone_number
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}







@router.post("/token", response_model=Token)
async def auth_user_token(
    formdata: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = user_authenticate(formdata.username, formdata.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_access_token(user.Username, user.ID, user.Role, timedelta(minutes=20))
    return {"access_token": token, "access_type": "Bearer"}

    

    
@router.get("/current_user")
async def current_user_endpoint(current_user=Depends(get_current_user)):
    """
    Returns info about the currently logged-in user.
    Frontend calls this to display username, role, etc.
    """
    return current_user







    