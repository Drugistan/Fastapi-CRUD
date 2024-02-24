from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
from schemas import UserSchema, UserCreateSchema
from models import User
from connection import get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/users", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/users", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    u = User(name=user.name, email=user.email, password=user.password)
    db.add(u)
    db.commit()
    return u


@app.put("/users/{user_id}", response_model=UserSchema)
def update_users(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    is_user = db.query(User).filter(User.id == user_id).first()
    print(user.email)
    if is_user:
        is_user.name = user.name
        is_user.email = user.email
        db.add(is_user)
        db.commit()
        return is_user
    raise HTTPException(status_code=400, detail="Not User")


@app.delete("/users/{user_id}", response_class=JSONResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        is_user = db.query(User).filter(User.id == user_id).first()
        db.delete(is_user)
        db.commit()
        return {"User is deleted": True}
    except:
        return HTTPException(status_code=400, detail="Not User")
