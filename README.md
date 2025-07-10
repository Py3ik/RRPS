# Refund Request Processing System (RRPS)

A system for managing refund requests. Supports registration, authentication, asynchronous IBAN validation, filtering, pagination, and CSV export. Built with Django, with the ability to switch between SQLite and PostgreSQL.

---

## Features

- User registration and authentication
- Create refund requests with IBAN validation via Abstract API
- List of requests with status filtering and pagination (20 records)
- Admin panel with filters, search, and CSV export
- Password reset (emails sent to console)
- Switch between SQLite and PostgreSQL via `.env`
- Code follows PEP 8 and is formatted with Black

---

## Requirements

- Python 3.13
- PostgreSQL (if `USE_SQLITE=False`)
- Dependencies: see `requirements.txt`

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Py3ik/RRPS.git
    cd RRPS
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the refund_system:**
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

    - For SQLite: `USE_SQLITE=True`
    - For PostgreSQL: make sure the database is set up (`psql -U py3ik -d refund_db`)
    - Replace `ABSTRACT_API_KEY` with your Abstract API key
    - Replace `SECRET_KEY` with your own secret

---

## Setup

1. **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

---

## Running

```bash
python manage.py runserver
```

- App: [http://127.0.0.1:8000/refunds/](http://127.0.0.1:8000/refunds/)
- Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Usage

- **Registration:** `/accounts/register/` — create an account, data is preserved on error
- **Login:** `/accounts/login/`
- **Create request:** `/refunds/create/` — IBAN is validated asynchronously
- **List requests:** `/refunds/` — filtering and pagination
- **Password reset:** `/accounts/password_reset/` — email sent to console
- **Admin panel:** filters, search, CSV export

---

## Testing

- **Registration:** check data preservation on invalid password
- **IBAN:** valid (`DE89370400440532013000`) and invalid (`XX123`) on `/refunds/create/`
- **Database:**
  - SQLite: `USE_SQLITE=True`, check `db.sqlite3`
  - PostgreSQL: `USE_SQLITE=False`, check `psql -U py3ik -d refund_db`
- **Admin panel:** filters, CSV export

---

## Formatting

- Code: PEP 8, Black
- Migrations excluded via `pyproject.toml`
- Formatting:
  ```bash
  black .
  black --check .
  ```