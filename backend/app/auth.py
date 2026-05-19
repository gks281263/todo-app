import datetime
import uuid
import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User

# Using Bearer scheme, but we don't need to be too pedantic about the exact credentials object
bearer_scheme = HTTPBearer()

def verify_pw(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def hash_pw(password: str) -> str:
    # Just standard bcrypt, nothing fancy
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_token(user_id: uuid.UUID) -> str:
    # simple exp time
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": str(user_id), "exp": exp}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")

def get_current_user(token=Depends(bearer_scheme), db: Session = Depends(get_db)):
    auth_err = HTTPException(status_code=401, detail="Invalid token")
    
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=["HS256"])
        uid = payload.get("sub")
        if not uid:
            raise auth_err
    except jwt.PyJWTError:
        raise auth_err

    # look up the user
    user = db.get(User, uuid.UUID(uid))
    if not user:
        raise auth_err
        
    return user
