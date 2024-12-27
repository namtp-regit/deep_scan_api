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
        self.session = session

    def make_new_query(self):
        return self.session.query(User)

    def filter_by_email(self, query, filter):
        if filter:
            return query.filter(self.model.email == str(filter))
        return query

    def get_users(self):
        users = self.session.query(User).all()
        return users

    def create_user_transaction(self, user_data: CreateUserRequest):
        try:
            with self.session.begin():
                existing_user = self.session.query(User).filter_by(email=user_data.email).first()
                if existing_user:
                    raise_exception(status.HTTP_400_BAD_REQUEST, "Email already registered")

                user = User(name=user_data.username, email=user_data.email)
                self.session.add(user)
                return user

        except Exception as e:
            self.session.rollback()
            raise_exception(
                status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed to create user: {str(e)}"
            )

    def create_user(self, user: CreateUserRequest):
        userCreate = User(**user.model_dump())
        self.session.add(userCreate)
        self.session.commit()
        self.session.refresh(userCreate)
        return userCreate

    def get_user(self, user_id: int):
        user = self.session.get(User, user_id)
        if not user:
            raise_exception(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    def update_user(self, user_id: int, user_data: UpdateUserRequest):
        user = self.session.get(User, user_id)
        if not user:
            raise_exception(status.HTTP_404_NOT_FOUND, "User not found")
        user_dump = user_data.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_dump)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.session.get(User, user_id)
        if not user:
            raise_exception(status.HTTP_404_NOT_FOUND, "User not found")
        self.session.delete(user)
        self.session.commit()
        return {"ok": True}
