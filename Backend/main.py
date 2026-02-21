from fastapi import FastAPI

from database import engine
import models
from routers import auth, todos, admin, users

from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()



# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




models.Base.metadata.create_all(bind=engine)

@app.get("/healthy")
async def healthy():
    return {"status":"healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
# app.include_router(rag_model.router)








    






