# Система запросов на возврат (RRPS)

Система для управления запросами на возврат средств. Поддерживает регистрацию, авторизацию, асинхронную валидацию IBAN, фильтрацию, пагинацию и экспорт в CSV. Использует Django с возможностью переключения между SQLite и PostgreSQL.

---

## Возможности

- Регистрация и авторизация пользователей
- Создание запросов на возврат с проверкой IBAN через Abstract API
- Список запросов с фильтрацией по статусу и пагинацией (20 записей)
- Админ-панель с фильтрами, поиском и экспортом в CSV
- Восстановление пароля (письма в консоли)
- Переключение между SQLite и PostgreSQL через `.env`
- Код соответствует PEP 8, отформатирован Black

---

## Требования

- Python 3.13
- PostgreSQL (если `USE_SQLITE=False`)
- Зависимости: см. `requirements.txt`

---

## Установка

1. **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Py3ik/RRPS.git
    cd RRPS
    ```

2. **Создайте виртуальное окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Создайте файл `.env` в корне:**
    ```env
    SECRET_KEY=''
    USE_SQLITE=False
    DB_NAME='refund_db'
    DB_USER='py3ik'
    DB_PASSWORD=''
    DB_HOST='localhost'
    DB_PORT='5432'
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL='refund@gmail.com'
    ABSTRACT_API_KEY=''
    DEBUG=True
    ```

    - Для SQLite: `USE_SQLITE=True`
    - Для PostgreSQL: убедитесь, что база настроена (`psql -U py3ik -d refund_db`)
    - Замените `ABSTRACT_API_KEY` на свой ключ от Abstract API
    - Замените `SECRET_KEY` на свой ключ

---

## Настройка

1. **Примените миграции:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2. **Создайте суперпользователя:**
    ```bash
    python manage.py createsuperuser
    ```

---

## Запуск

```bash
python manage.py runserver
```

- Приложение: [http://127.0.0.1:8000/refunds/](http://127.0.0.1:8000/refunds/)
- Админ-панель: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Использование

- **Регистрация:** `/accounts/register/` — создание аккаунта, данные сохраняются при ошибке
- **Авторизация:** `/accounts/login/`
- **Создание запроса:** `/refunds/create/` — IBAN проверяется асинхронно
- **Список запросов:** `/refunds/` — фильтрация и пагинация
- **Восстановление пароля:** `/accounts/password_reset/` — письмо в консоли
- **Админ-панель:** фильтры, поиск, экспорт CSV

---

## Тестирование

- **Регистрация:** проверьте сохранение данных при неверном пароле
- **IBAN:** валидный (`DE89370400440532013000`) и невалидный (`XX123`) на `/refunds/create/`
- **База:**
  - SQLite: `USE_SQLITE=True`, проверьте `db.sqlite3`
  - PostgreSQL: `USE_SQLITE=False`, проверьте `psql -U py3ik -d refund_db`
- **Админ-панель:** фильтры, экспорт CSV

---

## Форматирование

- Код: PEP 8, Black
- Миграции исключены через `pyproject.toml`
- Форматирование:
  ```bash
  black .
  black --check .
  ```