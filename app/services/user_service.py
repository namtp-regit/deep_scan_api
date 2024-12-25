from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.User import User
from app.requests.user_request import CreateUserRequest, UpdateUserRequest
from fastapi import HTTPException, status


def get_users(db: Session):
    users = db.query(User).all()
    return users


def create_user_transaction(user_data: CreateUserRequest, db: Session):
    try:
        with db.begin():
            existing_user = db.query(User).filter_by(email=user_data.email).first()
            if existing_user:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already registered")

            user = User(name=user_data.username, email=user_data.email)
            db.add(user)
            return user

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create user: {str(e)}"
        )


def create_user(user: CreateUserRequest, db: Session):
    userCreate = User.model_validate(user)
    db.add(userCreate)
    db.commit()
    db.refresh(userCreate)
    return userCreate


def get_user(user_id: int, db: Session):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def update_user(user_id: int, user_data: UpdateUserRequest, db: Session):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    user_dump = user_data.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_dump)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(user_id: int, db: Session):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}
