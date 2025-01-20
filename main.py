from fastapi import FastAPI, Form, File, UploadFile, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional



DATABASE_URL = "sqlite:///./test.db"  # SQLite fayl uchun yo'l

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite uchun maxsus parametr
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)


async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


class UserCreate(BaseModel):
    name: str
    password: str = Field(..., min_length=5, max_length=16)

    @field_validator("name")
    def name_must_not_empty(cls, v):
        if not v:
            raise ValueError("Name must not empty")
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    password: str

    class Config:
        orm_mode = True


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users    

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]



@app.put("/users/{user_id}", response_model=UserResponse)   
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.name:
        db_user.name = user.name
    if user.password:
        db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}



@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

#upload file 
# from fastapi import FastAPI, File, UploadFile   
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

# save file
@app.post("/savefile/")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(file.file.read())
    return {"filename": f"file {file.filename} saved successfully"}




@app.get("/")
def read_root():
    return {"Hello": "World"}

#@app.post("/user/")
#async def create_user(user: User):
#    return {"name": user.name, "password": user.password}

@app.put("/user/{user_id}")
async def update_user(user_id: int, name: str, passsword: str):
    return {"user_id": user_id, "name": name, "password": passsword}

@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    return {"user_id": f"user id: {user_id} deleted succesfully"}

#@app.get("/user/{user_item}")
#async def read_user(user_item: str):
 #   return {"user_id": user_item}

#@app.get("/user/")
#async def read_user(user_id: int, name: str=None):
#    return {"user_id": user_id, "name": name}