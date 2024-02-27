## Инструкция для запуска автотестов:

1. Выполнить команду для установки всех зависимостей
   ```shell
   pip install -r requirements.txt
2. Запустить api-тесты из корневой директории, выполнив команду, где 5 - количество потоков для параллельного запуска

   ```shell
   pytest -n 5

3. Сгенерировать отчёт после выполнения тестов и поднять Allure-сервер с результатами
   ```shell
   allure serve
