from fastapi import APIRouter, HTTPException, Response, BackgroundTasks, Depends, Form
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError

from models import *
from database import Session, get_session
from dependencies import verify_token, verify_turnstile_token
from utils import pwd_context, generate_jwt, send_email


router = APIRouter(tags=["Authentication"], prefix="/auth")

@router.post("/register", status_code=201, response_model=UserRead, dependencies=[Depends(verify_turnstile_token)])
def register(user: UserCreate, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already in use")
    background_tasks.add_task(send_email, email_to=db_user.email, subject="Verify your account", template="verify.html", context={"token": generate_jwt({"user_id": db_user.id})})
    return db_user

@router.post("/login", response_model=UserRead, dependencies=[Depends(verify_turnstile_token)])
def login(response: Response, username: str = Form(), password: str = Form(), session: Session = Depends(get_session)):
    statement = select(User).where(or_(User.username == username, User.email == username))
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if not db_user.is_verified:
        raise HTTPException(status_code=400, detail="User not verified")
    response.set_cookie(key="session_id", value=generate_jwt({"user_id": db_user.id}, audience="login"))
    return db_user

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="session_id")
    return {"status": "success", "message": "Logged out"}

@router.post("/verify/{token}")
def verify(token: int = Depends(verify_token), session: Session = Depends(get_session)):
    db_user = session.get(User, token)
    if db_user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    db_user.is_verified = True
    session.add(db_user)
    session.commit()
    return {"status": "success", "message": "User verified"}

@router.post("/forgot-password", dependencies=[Depends(verify_turnstile_token)])
def forgot_password(email: EmailStr, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    background_tasks.add_task(send_email, email_to=db_user.email, subject="Reset your password", template="reset_password.html", context={"token": generate_jwt({"user_id": db_user.id})})
    return {"status": "success", "message": "Email sent"}

@router.post("/reset-password/{token}")
def reset_password(password: str, token: int = Depends(verify_token), session: Session = Depends(get_session)):
    db_user = session.get(User, token)
    db_user.password = pwd_context.hash(password)
    session.add(db_user)
    session.commit()
    return {"status": "success", "message": "Password reset"}