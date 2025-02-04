# deep_scan_api

A new FastApi project.

---

## Setup project
```bash
# create virtual environment
$ python -m venv venv

# linux, macos
$ source .venv/bin/activate
# window powershell
$ .venv\Scripts\Activate.ps1
# window bash
$ source venv/Scripts/activate

# note: save package after install new
$ pip freeze > requirements.txt
```

```bash
# add package dependencies
$ pip install -r requirements.txt
```

```bash
# create jwt secret-key
$ openssl rand -base64 32
```

```bash
# migration
# create
$ alembic revision --autogenerate -m "Add users table"
# history
$ alembic history
# back
$ alembic downgrade
# run
$ alembic upgrade head
```

```bash
# seeder
$ python -m database.seeds.admin
```

```bash
# run formatter
$ black .
```

## Running the app

```bash
# development
$ uvicorn main:app --host 127.0.0.1 --port 8004 --reload
```

## Env
```bash
# .env
APP_NAME=
DEBUG=

DB_CONNECTION=
DB_HOST=
DB_PORT=
DB_DATABASE=
DB_USERNAME=
DB_PASSWORD=

SECRET_KEY=
ALGORITHM=
EXPIRE=

TIMEZONE=

MAIL_MAILER=
MAIL_HOST=
MAIL_PORT=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_ENCRYPTION=
MAIL_FROM_ADDRESS=
MAIL_FROM_NAME=

ALLOWED_CONTENT_TYPES=
MAX_FILE_SIZE=
```

## Build App
### dev
```bash
# Debug
```

### Prerequisites
