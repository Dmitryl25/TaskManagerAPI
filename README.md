# TaskManagementAPI

REST API для управления задачами в команде. Проект создан для изучения и практики backend-разработки на Python с использованием современного async-стека.

## Стек технологий

- **FastAPI** — основной фреймворк
- **PostgreSQL** — основная база данных
- **SQLAlchemy** (async) + **Alembic** — ORM и миграции
- **Redis** — хранение refresh-токенов
- **Celery** + **Celery Beat** — фоновые задачи и периодические задачи
- **Flower** — мониторинг Celery
- **MinIO** — объектное хранилище для файловых вложений (S3-совместимое)
- **WebSocket** — уведомления в реальном времени
- **slowapi** — rate limiting
- **structlog** — структурированное логирование
- **JWT** — аутентификация (access + refresh токены)
- **pytest** + **pytest-asyncio** — тесты

## Функциональность

- Регистрация и аутентификация пользователей (JWT, refresh/logout)
- Управление workspace: создание, редактирование, удаление, управление участниками и ролями
- Управление проектами внутри workspace
- Управление задачами: создание, фильтрация по статусу/приоритету/исполнителю/поиску
- Комментарии к задачам
- Файловые вложения к задачам через MinIO (presigned URL)
- WebSocket-уведомления при назначении исполнителя задачи
- Rate limiting на эндпоинтах авторизации
- Отправка email при регистрации через Celery

## Запуск

### Требования

- Docker и Docker Compose

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd TaskManagementAPI
```

### 2. Создать `.env` файл

```env
POSTGRES_DB=teamflow
POSTGRES_USER=admin
DB_PASSWORD=postgres
POSTGRES_HOST=database
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis

SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHMS=HS256

S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_ENDPOINT=http://minio:9000
S3_BUCKET=attachments
```

### 3. Поднять все сервисы

```bash
docker compose up -d
```

### 4. Создать бакет в MinIO

Открыть `http://localhost:9001` в браузере, войти с логином/паролем из `.env` (`S3_ACCESS_KEY` / `S3_SECRET_KEY`) и создать бакет с именем `attachments`.

### 5. API готово

```
http://localhost:8000
http://localhost:8000/docs   # Swagger UI
```

Мониторинг Celery: `http://localhost:5555`

## Запуск тестов

Для тестов нужен локальный PostgreSQL на порту `5433`. Добавить в `.env`:

```env
TEST_POSTGRES_DB=teamflow_test
TEST_POSTGRES_USER=admin
TEST_DB_PASSWORD=postgres
TEST_POSTGRES_HOST=127.0.0.1
TEST_POSTGRES_PORT=5433
```

```bash
pytest tests/ -v
```

## Структура проекта

```
app/
├── api/
│   ├── routers/      # эндпоинты
│   └── deps.py       # зависимости FastAPI
├── core/
│   ├── config.py     # настройки из .env
│   ├── security.py   # JWT
│   ├── s3.py         # клиент MinIO
│   ├── limiter.py    # rate limiting
│   └── logger.py     # structlog
├── models/           # SQLAlchemy модели
├── repositories/     # слой работы с БД
├── services/         # бизнес-логика
└── schemas/          # Pydantic схемы
```
