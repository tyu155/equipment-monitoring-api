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


## Следующие самостоятельные улучшения
- Фильтрация оборудования по статусу и пагинация.
- Сортировка измерений.
- Новая колонка `description` через миграцию.
- Авторизация пользователей.
- Интеграционные тесты на PostgreSQL.
- CI для автоматического запуска тестов.
