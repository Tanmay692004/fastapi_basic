from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from typing import Optional
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import JSONResponse



app = FastAPI()

class Userclass(BaseModel):
    name: str
    age: int
    email: str
    bio: Optional[str] = "No Bio Provided"
    active: bool = True
    @field_validator("age")
    @classmethod
    def age_positive(cls, value):
        if value <=0:
            raise ValueError("nakli admi")
        return value

class UserResponse(BaseModel):
    name: str
    email: str
    message: str
    
class Usernotactive(Exception):
    pass   



@app.get("/")
async def root():
    return {"message": "hello tanmay"}

@app.get("/square")
async def square(num: int):
    return {"input": num, "square": num**2}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"hello, {name}"}

@app.post("/create-user")
async def create_user(user:Userclass):
    return {"message": "user created successfully", "user": user,}

@app.post("/update-user")
async def update(user: Userclass, notify: bool= False):
    return {"updated user": user, "notify user":notify}

@app.post("/register", response_model= UserResponse)
async def register(user: Userclass):
    return {"name": user.name, "email": user.email, "message": "registration successful"}

@app.post("/login", status_code=status.HTTP_201_CREATED)
async def login():
    return {"message": "login successful"}

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    if user_id not in [2,3,1,6]:
        raise HTTPException(status_code=404, detail="user not found")
    return {"user": {"id": sum({user_id}), "name": "Tanmay"}}

@app.exception_handler(Usernotactive)
async def usernotactive_handler(request, exc):
    return JSONResponse(status_code = 400, content = {"message": "user inactive. sorry bro"},)

@app.post("/check")
async def check_user(user: Userclass):
    if not user.active:
        raise Usernotactive()
    return {"message": "user is active", "user":user}