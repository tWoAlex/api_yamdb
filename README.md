## API для проекта YaTube

Проект является бэкендом простой соцсети, включает в себя базу данных и открытый API.
Позволяет запустить простую соцсеть с постами и комментариями, а также системой подписок.

### API позволяет:
* Получить все опубликованные посты
* Публиковать посты
* Публиковать комментарии к постам
* Подписываться на авторов

### Документация проекта:
Доступна по адресу
```
http://127.0.0.1:8000/redoc/
```
После запуска проекта.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/tWoAlex/api_final_yatube.git
```
```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
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

### Примеры запросов:
Публикация поста:
```
POST /api/v1/posts/
Тело: { "text": "Текст вашего поста", "image": "Файл картинки", "group": ID группы }
```
Запрос постов:
```
GET /api/v1/posts/
```
```
Ответ: [
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "pub_date": "2021-10-14T20:41:29.648Z",
    "image": "string_base64",
    "group": 0
  }
]
```
Просмотр комментариев:
```
GET /api/v1/posts/{post_id}/comments/
```
```
Ответ: [
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]
```
Подписка на автора:
```
POST /api/v1/follow/
```
```
Тело: { "following": "username" }
```

### Использованные технологии:
* Django 3.2.16
* Django Rest Framework 3.12.4
* Djoser 2.1.0