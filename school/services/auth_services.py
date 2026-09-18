from datetime import date

from school.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token
from school.models.users import User


class AuthServices:

    @staticmethod
    def create_user(data):

        full_name = data.get("full_name")
        email = data.get("email")
        phone_number = data.get("phone_number")
        date_of_birth = data.get("date_of_birth")
        role = data.get("role", "STUDENT")
        password = data.get("password")

        if isinstance(date_of_birth, str):
            date_of_birth = date.fromisoformat(date_of_birth)

        if UserRepository.get_by_email(email):
            raise ValueError("USER ALREADY EXIST!")

        user = User(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            role=role,
        )

        user.users_password(password)

        try:
            UserRepository.create(user)
            UserRepository.commit()
            return user

        except:
            UserRepository.rollback()
            raise
        
    @staticmethod
    def login(data):

        email = data.get("email")
        password = data.get("password")

        user = UserRepository.get_by_email(email)

        if not user:
            raise ValueError("INVALID USER")

        if not user.verify_users_password(password):
            raise ValueError("INVALID PASSWORD OR EMAIL")

        return create_access_token(
            identity=str(user.id),
            additional_claims={
                "role" : user.role
            }
        )