# Продуктовый помощник - Foodgram!

**Описание проекта**
Продуктовый помощник, сайт, на котороым люди могут создавать и обмениваться своими рецептами, подписываться друг на друга, добавлять рецепты в избранное. Наш сервис позволит создавать список продуктов, нужных для определенного блюда.

**Как запустить проект локально?**

**Создать и активировать виртуальное окружение:**

```
python3 -m venv env для mac/linux
python -m venv venv windows
source venv/Scripts/activate
```

**Установить зависимости из файла requirements.txt:**

```
pip install -r requirements.txt
```

**Выполнить миграции:**

```
python3 manage.py migrate для mac/linux
python manage.py migrate для windows
```

**Запустить проект:**

```
cd backend/
python3 manage.py runserver для mac/linux
python manage.py runserver для windows
```


**Шаблон env-файла.**

```
Он находится в папке infra
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=пользователь 
POSTGRES_PASSWORD=пароль 
DB_HOST=db 
DB_PORT=5432
```

**Как запускать проект?**

```
cd backend/
docker-compose up
```

**IP для подключения.**

 51.250.26.158
http://foodwithmunkushi.ddns.net/

**Используемые технологии(стэк):**

Python
Django(DRF, ORM)
Postgresql
Docker
Nginx
