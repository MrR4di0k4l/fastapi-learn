from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyQuery
from sqlalchemy.orm import Session
from users.models import UserModel
from core.database import get_db

header_scheme = APIKeyQuery(name="apikey")
# تابع برای دریافت کاربر جاری
def get_current_user(credentials = Depends(header_scheme), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == credentials).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user