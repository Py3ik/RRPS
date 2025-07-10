Система запросов на возврат
Система для создания, управления и администрирования запросов на возврат средств. Поддерживает регистрацию пользователей, валидацию IBAN через API, фильтрацию, пагинацию и экспорт данных в CSV. Использует Django с возможностью переключения между SQLite и PostgreSQL.
Возможности

Регистрация и авторизация пользователей.
Создание запросов на возврат с асинхронной проверкой IBAN через Abstract API.
Список запросов с фильтрацией по статусу и пагинацией (20 записей на страницу).
Админ-панель с фильтрами, поиском и экспортом в CSV.
Восстановление пароля через email (консольный бэкенд для тестов).
Переключение между SQLite и PostgreSQL через .env.
Код отформатирован по PEP 8 с помощью Black.

Требования

Python 3.13
PostgreSQL (опционально, если не используется SQLite)
Зависимости: см. requirements.txt

Установка

Клонируй репозиторий:git clone <your-repo-url>
cd refund-request-system


Создай виртуальное окружение:python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate


Установи зависимости:pip install -r requirements.txt


Создай файл .env в корне проекта:cp .env.example .env

Настрой .env:SECRET_KEY='your-secret-key-here'
USE_SQLITE=True
DB_NAME='refund_db'
DB_USER='py3ik'
DB_PASSWORD=''
DB_HOST='localhost'
DB_PORT='5432'
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT='587'
EMAIL_USE_TLS=True
EMAIL_HOST_USER='your-email@gmail.com'
EMAIL_HOST_PASSWORD='your-app-password'
DEFAULT_FROM_EMAIL='your-email@gmail.com'
ABSTRACT_API_KEY='your-abstract-api-key'


Для SQLite: USE_SQLITE=True.
Для PostgreSQL: USE_SQLITE=False, настрой базу через DB_*.
Замени ABSTRACT_API_KEY на ключ от Abstract API.
Для email используй пароль приложения Gmail или оставь консольный бэкенд.



Настройка

Примени миграции:python manage.py makemigrations
python manage.py migrate


Создай суперпользователя:python manage.py createsuperuser


(Опционально) Отформатируй код:black .



Запуск
python manage.py runserver


Доступ к приложению: http://localhost:8000.
Админ-панель: http://localhost:8000/admin/.

Использование

Регистрация: Перейди на /accounts/register/ и создай аккаунт.
Авторизация: Войди через /accounts/login/.
Создание запроса: На /refunds/create/ заполни форму (IBAN проверяется асинхронно).
Список запросов: Просмотри свои запросы на /refunds/ с фильтрацией и пагинацией.
Восстановление пароля: Используй /accounts/password_reset/ (письмо в консоли).
Админ-панель: Управляй запросами, фильтруй, экспортируй в CSV.

Тестирование

Проверь регистрацию: Создай пользователя, убедись, что данные сохраняются при ошибке.
Проверь IBAN: Введи валидный (DE89370400440532013000) и невалидный IBAN на /refunds/create/.
Проверь базу:
SQLite: Убедись, что db.sqlite3 создаётся (USE_SQLITE=True).
PostgreSQL: Проверь подключение (psql -U py3ik -d refund_db).


Проверь админ-панель: Фильтры, поиск, экспорт CSV.

Структура проекта
refund-request-system/
├── apps/
│   ├── accounts/
│   └── refunds/
├── refund_system/
├── templates/
├── static/
├── .env
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── manage.py

Форматирование

Код отформатирован Black (PEP 8).
Миграции исключены из форматирования через pyproject.toml.

Лицензия
MIT License