import string
from faker import Faker

faker_instance = Faker()


class DataGenerator:
    """
    Фейкер для генерации случайных данных
    """

    @staticmethod
    def fake_id():
        """
        Генерация случайного идентификатора
        """
        first_letter = faker_instance.random.choice(string.ascii_letters)
        rest_characters = ''.join(faker_instance.random.choices(string.ascii_letters + string.digits, k=10))
        fake_id = first_letter + rest_characters
        return fake_id

    @staticmethod
    def fake_name():
        """
        Генерация случайного имени
        """
        return faker_instance.word()

    @staticmethod
    def fake_email():
        """
        Генерация случайного email
        """
        return faker_instance.email()

    @staticmethod
    def fake_description(n=1):
        """
        Генерация случайного описания
        :param n: количество генерируемых предложений. По умолчанию 1
        :return: возвращается список предложений
        """
        return ' '.join(faker_instance.sentences(n))
