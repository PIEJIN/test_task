## Запуск проекта

Перед тем как начать, убедитесь, что у вас установлен Python и pip.

1. **Создайте виртуальное окружение:**

    ```bash
    python -m venv venv
    ```

2. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Примените миграции:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Создайте суперпользователя:**

    ```bash
    python manage.py createsuperuser
    ```

5. **Запустите сервер:**

    ```bash
    python manage.py runserver
    ```

Теперь ваш сервер запущен и готов к использованию!

### Авторизация

Для доступк API авторизуйтесь по адресу `/api/login/`.




