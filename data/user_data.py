from enums.roles import Roles
from utils.data_generator import DataGenerator


class UserData:
    @staticmethod
    def create_user_data(role=Roles.SYSTEM_ADMIN.value, scope="g"):
        return {
            "username": DataGenerator.fake_name(),
            "password": DataGenerator.fake_id(),
            "email": DataGenerator.fake_email(),
            "roles": {
                "role": [
                    {
                        "roleId": role,
                        "scope": scope
                    }
                ]
            }
        }
