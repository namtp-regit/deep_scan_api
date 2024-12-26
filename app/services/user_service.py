from sqlalchemy.orm import Session
from app.models.User import User
from fastapi import status
from app.requests.user_request import CreateUserRequest, UpdateUserRequest
from app.services.base_service import BaseService
from core.send_response import raise_exception


class UserService(BaseService):
    def __init__(self, session: Session):
        super().__init__(User, session)
        self.search_ables = ["name", "email"]
        self.filter_ables = {"email": self.filter_by_email}
        self.order_ables = {"name": "name", "created_at": "created_at"}

    def make_new_query(self):
        return self.session.query(User)

    def filter_by_email(self, query, filter):
        if filter:
            return query.filter(self.model.email == str(filter))
        return query

    def get_users(db: Session):
        users = db.query(User).all()
        return users

    def create_user_transaction(user_data: CreateUserRequest, db: Session):
        try:
            with db.begin():
                existing_user = db.query(User).filter_by(email=user_data.email).first()
                if existing_user:
                    raise_exception(status.HTTP_400_BAD_REQUEST, "Email already registered")

                user = User(name=user_data.username, email=user_data.email)
                db.add(user)
                return user

        except Exception as e:
            db.rollback()
            raise_exception(
                status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed to create user: {str(e)}"
            )

    def create_user(user: CreateUserRequest, db: Session):
        userCreate = User(**user.model_dump())
        db.add(userCreate)
        db.commit()
        db.refresh(userCreate)
        return userCreate

    def get_user(user_id: int, db: Session):
        user = db.get(User, user_id)
        if not user:
            raise_exception(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    def update_user(user_id: int, user_data: UpdateUserRequest, db: Session):
        user = db.get(User, user_id)
        if not user:
            raise_exception(status.HTTP_404_NOT_FOUND, "User not found")
        user_dump = user_data.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_dump)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def delete_user(user_id: int, db: Session):
        user = db.get(User, user_id)
        if not user:
            raise_exception(status.HTTP_404_NOT_FOUND, "User not found")
        db.delete(user)
        db.commit()
        return {"ok": True}
