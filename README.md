# Testproject_Wallet

Простое FastAPI приложение для управления кошельками с поддержкой асинхронных операций и баланса.

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-7%20passed-brightgreen)](tests/)

## Функциональность

- **GET /api/v1/wallets/{wallet_uuid}** — получение баланса кошелька
- **POST /api/v1/wallets/{wallet_uuid}/operation** — пополнение (DEPOSIT) или снятие (WITHDRAW) средств

## Технологии

- **Python 3.12**
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM для работы с БД
- **Alembic** — миграции базы данных
- **PostgreSQL** — основная база данных
- **Docker / Docker Compose** — контейнеризация
- **Pytest** — тестирование

## Быстрый старт с Docker

### Предварительные требования

- Установленные [Docker](https://www.docker.com/products/docker-desktop/) и [Docker Compose](https://docs.docker.com/compose/)

### Запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/SergeyGusev1/Testproject_Wallet.git
   cd Testproject_Wallet
   ```
Запустите контейнеры:
```bash
docker-compose up --build
```
Приложение будет доступно по адресу: http://localhost:8000

Документация API (Swagger): http://localhost:8000/docs

Запуск без Docker (для разработки)
Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
Установите зависимости:
```bash
pip install -r requirements.txt
```
Настройте PostgreSQL и создайте базу данных wallet_db.

Создайте файл .env из примера:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/wallet_db
```
Примените миграции:
```bash
alembic upgrade head
```
Запустите сервер:
```bash
uvicorn app.main:app --reload
```
Тестирование
```bash
pytest tests/ -v
```
Структура 
```bash
Testproject_Wallet/
├── app/                    # Основной код приложения
│   ├── core/               # Конфигурация, БД, базовые модели
│   ├── models/             # Модели SQLAlchemy
│   ├── schemas/            # Схемы Pydantic
│   └── main.py             # Точка входа
├── alembic/                 # Миграции Alembic
├── tests/                   # Тесты
├── .env.example             # Пример переменных окружения
├── .gitignore               # Исключенные файлы
├── Dockerfile               
├── docker-compose.yml
├── requirements.txt
└── README.md                # Этот файл
```