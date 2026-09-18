from school.repositories.user_repository import UserRepository

class UserServices:

    @staticmethod
    def get_user_by_id(user_id):

        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError(
                "User not found"
            )
        return user

    @staticmethod
    def get_all_user():
        return UserRepository.get_all()

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None

        user.full_name = data.get("full_name", user.full_name)
        user.email = data.get("email", user.email)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.date_of_birth = data.get("date_of_birth", user.date_of_birth)
        UserRepository.commit()
        return user

    @staticmethod
    def delete_user(user_id):

        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError(
                "User Not Found!"
            )

        UserRepository.delete(user)
        return user