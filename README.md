# _YaMDb_ - платформа для сбора отзывов на произведения.

### ОПИСАНИЕ ПРОЕКТА:

_YaMDb_ - платформа для сбора отзывов на произведения, которые в свою очередь делятся на категории и жанры.

Все пользователи имеют возможность не только оставить отзывы и оценивать произведения, но и прокомментировать отзывы других пользователей.


### УСТАНОВКА:

Чтобы развернуть проект на локальной машине, выполните следующие шаги:

- _Клонируйте репозиторий:_
```
git clone git@github.com:KPrima/api_yamdb1.git
```
- _Перейдите в директорию проекта:_
```
cd api_yamdb
```
- _Создайте виртуальное окружение:_
```
python -m venv venv
```
- _Активируйте виртуальное окружение:_

для Windows:
```
venv\Scripts\activate
```

для macOS и Linux:
```
source venv/bin/activate
```

- _Установите зависимости:_
```
pip install -r requirements.txt
```
- _Примените миграции базы данных:_
```
python manage.py migrate
```
- _Запустите сервер разработки:_
```
python manage.py runserver
```

### Примеры запросов к API:

* Регистрация пользователя с получением кода доступа на e-mail (POST-запрос):

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

* Получение JWT-токена в обмен на username и confirmation code (POST-запрос):

```
http://127.0.0.1:8000/api/v1/auth/token/
```

* Получение списка всех произведений (GET-запрос):

```
http://127.0.0.1:8000/api/v1/titles/
```

* Получение списка всех категорий (GET-запрос):

```
http://127.0.0.1:8000/api/v1/categories/
```

*С другими запросами к API можно ознакомиться в документе [ReDoc](http://127.0.0.1:8000/redoc/)*

### Использованные технологии:

- Python 3.9.10
- Django 3.2
- Django REST Framework 3.12.4
- Simple-JWT
- SQlite
- pytest

### Дополнительная  информация:

copyright = 2023, Andreychenko Anastasia, Kristina Prima, Vladislav Piyankov

author = [Andreychenko Anastasia](https://github.com/Maivery) (teamlead), [Kristina Prima](https://github.com/KPrima), [Vladislav Piyankov](https://github.com/BraziT)

release = '0.1.0'

language = 'ru'

Programming Language: Python 3
