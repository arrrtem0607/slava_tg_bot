# Магический Telegram-бот

Асинхронный Telegram-бот на базе `aiogram` и `aiogram_dialog`, который регистрирует пользователя, вычисляет его магическое число по дате рождения и показывает соответствующее описание судьбы из базы данных.

## Возможности
- Регистрация пользователя с сохранением данных в PostgreSQL;
- Вычисление магического числа по дате рождения;
- Получение описания судьбы из таблицы `fates` по магическому числу;
- Структура проекта готова к интеграции платёжного модуля.

## Требования
- Python 3.10+
- PostgreSQL 13+

> ⚠️ Проект требует `aiogram` версии **3.7.0** или новее. Для задания `parse_mode` и других
> параметров по умолчанию используются `DefaultBotProperties`.

## Настройка окружения
1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` на основе `.env.example` и укажите ваши значения:
   ```env
   BOT_TOKEN=your_bot_token_here
   DATABASE_URL=postgresql+asyncpg://magic_user:magic_pass@localhost:5432/magic_db
   ```
4. Выполните миграции (создайте таблицы) с помощью SQLAlchemy:
   ```bash
   python -m bot.manage_db
   ```
   > Для простоты можно выполнить SQL-скрипт `db/seed_fates.sql`, который создаёт таблицы и добавляет демо-данные.

## Запуск бота
```bash
python -m bot.main
```

## Структура проекта
```
project_root/
├── bot/
│   ├── main.py              # Точка входа бота
│   ├── handlers/            # Обработчики команд
│   ├── dialogs/             # Логика диалогов aiogram_dialog
│   ├── keyboards/           # Клавиатуры и кнопки
│   ├── lexicon/             # Тексты и сообщения бота
│   ├── services/            # Утилиты и вспомогательные сервисы
│   └── reading_env.py       # Загрузка переменных окружения
├── db/
│   ├── engine.py            # Настройка подключения к базе
│   ├── models.py            # ORM-модели SQLAlchemy
│   ├── orm.py               # Класс для взаимодействия с БД
│   └── seed_fates.sql       # Демо-данные для таблицы `fates`
├── payments/                # Заготовка для платёжного модуля
├── requirements.txt
├── .env.example
└── README.md
```

## Подготовка базы данных
### Автоматическое создание пользователя и базы
```bash
chmod +x scripts/setup_db.sh
./scripts/setup_db.sh
```

### Ручной сценарий
1. Подключитесь к PostgreSQL под пользователем `postgres`:
   ```bash
   psql -U postgres
   ```
2. Создайте пользователя `magic_user` и базу данных `magic_db` в PostgreSQL и выдайте права:
   ```sql
   CREATE USER magic_user WITH PASSWORD 'magic_pass';
   CREATE DATABASE magic_db OWNER magic_user;
   GRANT ALL PRIVILEGES ON DATABASE magic_db TO magic_user;
   ```
3. Выполните SQL-скрипт `db/seed_fates.sql`, который создаст таблицы и наполнит `fates` тестовыми значениями:
   ```bash
   psql -d magic_db -f db/seed_fates.sql
   ```

## Дополнительно
- В каталоге `payments/` находятся заглушки для будущей интеграции платежей.
- Все ключевые сообщения вынесены в `bot/lexicon/texts.py` для удобного редактирования.
- Логи записываются через стандартный модуль `logging`.
