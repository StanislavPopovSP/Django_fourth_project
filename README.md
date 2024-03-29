<h2 align="center">DevSearch</h2>


### Описание проекта:
Сайт для поиска разработчиков, на основе их проектов и их навыков.

Можно написать разработчику личное сообщение на сайте, перейти на его соцсеть, оценить комментарием его проект, найти по имени, описанию, навыкам.

### Функционал
- Авторизация, регистрация через форму
- Редактирование профиля пользователя
- Создать, редактировать и удалять
  - Навыки, их подробное описание
  - Данные о профиле
    - Имя, email, username, описание, фотографию профиля, соцсети
  - Проекты
    - Заголовок, изображение, описание, ссылку на проект, теги с его навыками
- Поиск разработчиков, проектов
- Пагинация
- Комментирование проекта
- Чтение входящего сообщения с самого сайта


### Инструменты разработки

**Стек:**
- Python >= 3.9
- Django == 4.2
- sqlite3

## Установка

##### 1) Клонировать репозиторий

    https://github.com/StanislavPopovSP/Django_fourth_project.git

##### 2) Создать виртуальное окружение

    python -m venv venv

##### 3) Активировать виртуальное окружение

Linux

    source venv/bin/activate

Windows

    ./venv/Scripts/activate

##### 4) Устанавливить зависимости:

    pip install -r requirements.txt

##### 5) Выполнить команду для выполнения миграций

    python manage.py migrate

##### 6) Создать суперпользователя

    python manage.py createsuperuser

##### 7) Запустить сервер

    python manage.py runserver

##### 8) Ссылки

- Сайт http://127.0.0.1:8000/

- Админ панель http://127.0.0.1:8000/admin
