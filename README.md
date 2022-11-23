[![API for YaMDB project workflow](https://github.com/Tozix/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=main)](https://github.com/Tozix/yamdb_final/actions/workflows/yamdb_workflow.yml)

# API сервис проекта YaMDB
Проект разработан командой мечты из трех разработчиков, в рамках обучения на курсе Backend-разработчик Яндекс Практикума.
___
### Описание
Это полноценный проект предоставляющий отзывы для различных произведений основанный исключительно на API. Благодаря API данные можно получать на различных ресурсах и что самое важное на различных устройствах. Любое мобильное приложение или веб сайт может пользоваться данными YaMBD, вносить изменения и быть в курсе новых отзывов и комментарий к произведениям. Блок аутентификации и авторизации выстроен просто для пользователя и в то же время защищает данные пользователей не позволяя сторонним пользователям изменять данные других пользователей. Для удобно поиска нужно произведения внедрены фильтры по жанрам и категориям. Ни одно произведение не останется без отзыва, а отзыв без комментария на всех видах устройств.
___
### Технологии
- [Python 3.7]
- [Django 3.2.15]
- [SimpleJWT 4.7.2]
- [Django REST Framework 3.12.4]
- [DRF multiple serializer 0.2.3]
- [Django-filters]
___


# Запуск проекта в dev-режиме на локальном сервере:
Клонировать репозиторий и перейти в директорию с ним:
```
git clone https://github.com/Tozix/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
Сервер будет доступен по адресу:
```
http://127.0.0.1:8000/
```
___
### Примеры GET запросов
Для получения списка доступных адресов отправьте запрос:
```
http://127.0.0.1:8000/api/v1/
```
Пример ответа на запрос о получении списка доступных адресов в формате json:
```
{
    "users": "http://127.0.0.1:8000/api/v1/users/",
    "titles": "http://127.0.0.1:8000/api/v1/titles/",
    "categories": "http://127.0.0.1:8000/api/v1/categories/",
    "genres": "http://127.0.0.1:8000/api/v1/genres/"
}
```
Для получения всех произведений:
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Пример ответа на запрос о получении всех произведений в формате json:
```
[
    {
        "count": 1,
        "next": "Null",
        "previous": "Null",
        "results": [
            {
                "id": 1,
                "name": "The best team",
                "year": 2022,
                "rating": 10,
                "description": "Little story about dev team",
                "genre": [
                    {
                        "name": "Adventure",
                        "slug": "adventure"
                    }
                ],
                "category": {
                "name": "IT",
                "slug": "it"
                }
            }
        ]
    }
]
```
Все виды запросов и их описание доступно в документации по адресу:
```
http://127.0.0.1:8000/redoc/
```
## Шаблон наполнения .env
```
# указываем, с какой БД работаем
DB_ENGINE=django.db.backends.postgresql
# имя базы данных
DB_NAME=
# логин для подключения к базе данных
POSTGRES_USER=
# пароль для подключения к БД (установите свой)
POSTGRES_PASSWORD=
# название сервиса (контейнера)
DB_HOST=
# порт для подключения к БД
DB_PORT=
```

## Автоматизация развертывания серверного ПО
Для автоматизации развертывания ПО на боевых серверах используется среда виртуализации Docker, а также Docker-compose - инструмент для запуска многоконтейнерных приложений. Docker позволяет «упаковать» приложение со всем его окружением и зависимостями в контейнер, который может быть перенесён на любую Linux -систему, а также предоставляет среду по управлению контейнерами. Таким образом, для разворачивания серверного ПО достаточно чтобы на сервере с ОС семейства Linux были установлены среда Docker и инструмент Docker-compose.

Ниже представлен Dockerfile - файл с инструкцией по разворачиванию Docker-контейнера веб-приложения:
```Dockerfile
# 3.7 — используемая версия Python.
# slim — обозначение того, что образ имеет только необходимые компоненты для запуска,
FROM python:3.7-slim
# Cлужебная информацию об образе.
LABEL author='Tozix' version=0.0.1Beta
# Сделать директорию /app рабочей директорией.
WORKDIR /app
# Копируем все содержимое папки в рабочую директорию
COPY ./ .
# Устанавливаем зависимости
RUN pip3 install -r requirements.txt --no-cache-dir
# Запускаем сервер gunicorn на порту 8000
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
```
В файле «docker-compose.yml» описываются запускаемые контейнеры: веб-приложения, СУБД PostgreSQL и сервера Nginx.
```Dockerfile
# версия docker-compose
version: '3.8'

# имена и описания контейнеров, которые должны быть развёрнуты
services:
  # описание контейнера db
  db:
    image: postgres:13.0-alpine
    volumes:
      - data_value:/var/lib/postgresql/data/
    env_file:
      - ./.env
  # описание контейнера web
  web:
    build: ../api_yamdb
    restart: always
    volumes:
      - static_value:/app/static/
      - media_value:/app/media/

    depends_on:
      - db
    env_file:
      - ./.env
  # описание контейнера nginx
  nginx:
    image: nginx:1.21.3-alpine
    ports:
      - "80:80"

    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_value:/var/html/static/
      - media_value:/var/html/media/

    depends_on:
      - web
# Список томов
volumes:
  data_value:
  static_value:
  media_value:


```

## Описание команд для запуска приложения в контейнерах
Для запуска проекта в контейнерах используем **docker-compose** : ```docker-compose up -d --build```, находясь в директории (infra_sp2) с ```docker-compose.yaml```

После сборки контейнеров выполяем:
```bash
# Выполняем миграции
docker-compose exec web python manage.py migrate
# Создаем суперппользователя
docker-compose exec web python manage.py createsuperuser
# Собираем статику со всего проекта
docker-compose exec web python manage.py collectstatic --no-input
# Для дампа данных из БД
docker-compose exec web python manage.py dumpdata > fixtures.json
```
### Для выгрузки данных из дампа (резервной копии) в БД
```bash
docker-compose exec web bash
# Сброс БД, суперюзеры так же удаляются
>>> python manage.py flush
>>> python manage.py loaddata fixtures.json
```


___
### Команда
- [Никита Емельянов], студент Яндекс Практикума он же тимлид на этом проекте.
- [Полина Костина], студентка Яндекс Практикума
- [Дмитрий Ротанин], студент Яндекс Практикума

[//]: # (Ниже находятся справочные ссылки)

   [Python 3.7]: <https://www.python.org/downloads/release/python-370/>
   [Django 3.2.15]: <https://www.djangoproject.com/download/>
   [SimpleJWT 4.7.2]: <https://django-rest-framework-simplejwt.readthedocs.io/en/latest/>
   [Django REST Framework 3.12.4]: <https://www.django-rest-framework.org/community/release-notes/>
   [DRF multiple serializer 0.2.3]: <https://pypi.org/project/drf-multiple-serializer/>
   [Django-filters]: <https://django-filter.readthedocs.io/en/stable/guide/install.html>
   [Никита Емельянов]: <https://github.com/Tozix>
   [Полина Костина]: <https://github.com/Polina1Kostina>
   [Дмитрий Ротанин]: <https://github.com/Annsjaw>
