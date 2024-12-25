import bcrypt
from sqlalchemy.orm import Session
from app.models.Admin import Admin
from database.connect import engine

data = {
    "name": "admin",
    "mail_address": "admin@regit-technology.com",
    "password": "12345678a@",
    "role": 1,
}


def seed_admin():
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode(
        'utf-8'
    )

    with Session(engine) as session:
        admin = session.query(Admin).filter_by(mail_address=data["mail_address"]).first()
        if admin:
            print("Admin existed")
            return

        # Create a new admin
        admin = Admin(
            name=data["name"],
            mail_address=data["mail_address"],
            password=hashed_password,
            role=data["role"],
        )
        session.add(admin)
        session.commit()
        print("Create account successfully!")


if __name__ == "__main__":
    seed_admin()
