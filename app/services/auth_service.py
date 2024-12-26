from sqlalchemy.orm import Session
from app.models.Admin import Admin
from fastapi import HTTPException, status
import bcrypt
from app.requests.login_request import LoginRequest, Token
from core.jwt_handler import create_access_token
from core.config import settings
from core.jwt_handler import blacklist
from core.send_response import raise_exception


def authenticate(db: Session, mail_address: str, password: str):
    admin = db.query(Admin).filter(Admin.mail_address == mail_address).first()
    if not admin:
        return None
    if not bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
        return None
    return admin


def login(db: Session, request: LoginRequest) -> Token:
    admin = authenticate(db, request.mail_address, request.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mail_address or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # create JWT token
    access_token = create_access_token(data={"sub": str(admin.id)})
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": settings.expire,
        "me": admin,
    }


def logout(token: str):
    if token in blacklist:
        raise_exception(status.HTTP_400_BAD_REQUEST, "Token is already revoked")
    blacklist.add(token)
    return {"message": "Logged out successfully!"}
