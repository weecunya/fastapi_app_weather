# FastAPI Weather & Auth Service 🌤️

Асинхронное веб-приложение на базе **FastAPI**, предоставляющее защищенный API для управления профилями пользователей и получения данных о погоде через интеграцию с внешним сервисом (Meteoblue API).

Проект демонстрирует навыки работы с асинхронным Python, базами данных, брокерами сообщений (Redis), а также реализации собственной системы сессионной аутентификации и Rate Limiting.

## Стек технологий

* **Backend:** Python 3.13, FastAPI, Pydantic
* **Database:** SQLite, SQLAlchemy 2.0 (async), aiosqlite
* **Caching & Sessions:** Redis (redis.asyncio)
* **External HTTP Requests:** aiohttp (асинхронные запросы к API погоды)
* **Frontend:** Статический HTML / CSS / Vanilla JS (подключен через StaticFiles)
* **Testing:** Pytest, HTTPX / Requests
* **Infrastructure:** Docker, Docker Compose

---

## Ключевые возможности (Features)

1. **Безопасная аутентификация (Session-based):**

* Отказ от JWT в пользу сессионных токенов (хранятся в Redis с TTL и дублируются в БД).
* Использование HTTPOnly Cookies для защиты от XSS атак.
* Надежное хеширование паролей (pbkdf2_hmac через встроенный модуль hashlib).

2. **Ограничение запросов (Rate Limiting):**

* Кастомная зависимость (Dependency) FastAPI, использующая Redis для ограничения количества запросов с одного IP-адреса (защита от брутфорса и спама внешнего API).

3. **Интеграция с Meteoblue API:**

* Асинхронный геокодинг (поиск координат по названию города) и получение прогноза погоды через aiohttp.
* Базовое in-memory кэширование результатов для снижения нагрузки на стороннее API.

4. **Управление профилем пользователя (CRUD):**

* Получение данных текущего пользователя (/users/me).
* Обновление профиля.
* Удаление аккаунта (включает инвалидацию сессий в БД и удаление токена из Redis).

---

## 🛠️ Структура проекта

* app/routers/ — маршрутизаторы FastAPI (auth, users, weather).
* app/models/ — декларативные модели SQLAlchemy.
* app/schemas/ — Pydantic схемы для валидации входящих/исходящих данных.
* app/clients/ — клиенты для внешних сервисов (Redis, Meteoblue API).
* app/dependencies.py — внедрение зависимостей (проверка текущего пользователя, Rate Limit, сессии БД).
* database.py — настройка асинхронного движка SQLAlchemy.
* static/ — простой фронтенд клиент для демонстрации работы API.
* tests/ — модульные (unit) и интеграционные (edge cases) тесты.

---

## ⚙️ Установка и запуск

Проект полностью докеризован. Для запуска вам понадобится установленный Docker и Docker Compose.

1. Клонируйте репозиторий:
2. 
git clone <URL-вашего-репозитория>
cd fastapi_app_weather

4. Настройте переменные окружения:
Создайте файл .env на основе примера и впишите туда ваш API-ключ от Meteoblue:

cp .env.example .env

Пример .env:

API_KEY=your_meteoblue_api_key
SECRET_KEY=your_super_secret_key
BASE_URL=http://localhost:8000
REDIS_URL=redis://redis:6379

3. Запустите контейнеры:
   
docker-compose up -d --build

После сборки и запуска приложение будет доступно по адресам:

* UI (Демо-фронтенд): http://localhost:8000
* API Документация (Swagger): http://localhost:8000/docs

---

## 🧪 Тестирование

В проекте настроен pytest для проверки API (регистрация, логин, права доступа, погодные эндпоинты).

Для запуска тестов выполните команду:

# Локальный запуск (если установлено виртуальное окружение)

pytest -v

# Или запуск внутри запущенного Docker контейнера

docker-compose exec app pytest -v

---

## 📈 Планы по развитию (TODO)

* Перенести кэширование погодных ответов из словаря (cash_dict в памяти) в Redis для поддержки многопроцессорного деплоя (Gunicorn/Uvicorn workers).
* Добавить админ-панель и ролевую модель (Role, UserRole — уже заложены в models.py).
* Настроить CI/CD (GitHub Actions / GitLab CI) для автоматического линтинга и тестирования.
