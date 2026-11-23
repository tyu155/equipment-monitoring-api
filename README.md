# Equipment Monitoring API

Учебный REST API для регистрации промышленного оборудования и хранения измерений температуры и давления.

> Учебная кодовая база создана с помощью AI-инструментов. 

## Возможности
- CRUD оборудования.
- Создание и просмотр истории измерений.
- Валидация данных через Pydantic.
- PostgreSQL и SQLAlchemy 2.x.
- Миграции Alembic.
- API-тесты Pytest + SQLite in-memory.
- Docker Compose для приложения и PostgreSQL.

## Запуск
Нужен Docker с Compose:

```bash
docker compose up --build
```

API: http://localhost:8000  
Swagger: http://localhost:8000/docs  
Health: http://localhost:8000/health

Остановить: `docker compose down`  
Удалить данные БД: `docker compose down -v`

## Локальный запуск
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```
Скопируйте `.env.example` в `.env`, настройте PostgreSQL, затем:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

## Маршруты
| Метод | Маршрут | Назначение |
|---|---|---|
| GET | `/health` | Проверка приложения |
| POST | `/api/v1/equipment` | Создать оборудование |
| GET | `/api/v1/equipment` | Список оборудования |
| GET | `/api/v1/equipment/{id}` | Получить оборудование |
| PATCH | `/api/v1/equipment/{id}` | Изменить оборудование |
| DELETE | `/api/v1/equipment/{id}` | Удалить оборудование |
| POST | `/api/v1/equipment/{id}/measurements` | Добавить измерение |
| GET | `/api/v1/equipment/{id}/measurements` | История измерений |

Пример создания:
```json
{
  "name": "Компрессор К-14",
  "location": "Цех №2",
  "status": "active",
  "serial_number": "CMP-00014"
}
```

Пример измерения:
```json
{"temperature": 72.5, "pressure": 4.8}
```

## Тесты
```bash
pytest -v
```

## Структура
```text
app/                 # приложение и API
app/routers/         # HTTP-маршруты
alembic/             # миграции
tests/               # тесты
Dockerfile
docker-compose.yml
requirements.txt
```

## Что изучить перед защитой
1. HTTP-методы и статус-коды 200, 201, 204, 404, 409, 422.
2. FastAPI, Pydantic и dependency injection через Depends.
3. SQLAlchemy Engine, Session, commit и rollback.
4. Первичный/внешний ключ и связь один-ко-многим.
5. Alembic-миграции.
6. Фикстуры Pytest и подмена зависимости БД.
7. Dockerfile и Docker Compose.

## Следующие самостоятельные улучшения
- Фильтрация оборудования по статусу и пагинация.
- Сортировка измерений.
- Новая колонка `description` через миграцию.
- Авторизация пользователей.
- Интеграционные тесты на PostgreSQL.
- CI для автоматического запуска тестов.
