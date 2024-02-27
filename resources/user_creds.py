import os
from dotenv import load_dotenv

load_dotenv()


class SuperAdminCreds:
    """
        Креды супер админа. Для авторизации в TeamCity под супер админом оставляется пустым username,
        а пароль - токен из логов контейнера
        """
    USERNAME = ''
    PASSWORD = os.getenv('SUPER_USER_TOKEN')
