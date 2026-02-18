from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models.user import User
from ..authentification.auth import hash_password, verify_password, create_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# request bodies for authentification
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Register endpoint
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if username exists
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash the password
        hashed = hash_password(user.password)

        new_user = User(username=user.username, hashed_password=hashed)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User registered successfully"}

    except Exception as e:
        print("Registration error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

# Login endpoint
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_token(db_user.username)
        return {"access_token": token}

    except Exception as e:
        print("Login error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")