from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserLogin
from app.core.security import verify_password
from app.core.security import create_access_token

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role="customer"
    )

    db.add(user)
    db.commit()

    return {
        "message": "User created"
    }

@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
    {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role
    }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role  
    }