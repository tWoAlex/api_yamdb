## API для проекта YaTube

Проект является бэкендом портала обзоров на различные произведения искусства, включающий систему публикации сведений о произведении, обзоров и комментариев к ним.
Включает в себя базу данных и открытый API.

### API позволяет:
* Администраторам: публиковать сведения о произведениях
* Получить сведения об оцениваемых произведениях
* Публиковать обзоры и рецензии
* Публиковать комментарии к обзорам и рецензиям

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
Публикация обзора:
```
POST /api/v1/titles/{title_id}/reviews/
Тело: { "text": "Текст вашего обзора", "score": "оценка произведения" }
```
Просмотр обзоров:
```
GET /api/v1/titles/{title_id}/reviews/
Ответ:
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
Публикация комментария:
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
Тело: { "text": "Текст вашего комментария" }
```
Просмотр комментариев:
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
Ответ:
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### Использованные технологии:
* Django 3.2
* Django Rest Framework 3.12.4
* DRF SimpleJWT 4.7.2
