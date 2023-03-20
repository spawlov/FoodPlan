# Сайт Подбора меню

Это сайт, который подберет вам оптимальное меню на каждый день.

Для запуска сайта необходимо

Создать файл .env в корне проекта (рядом с manage.py)
В нем прописать переменные:

```
SECRET_KEY=<Здесь должен быть секретный ключ Django>
DEBUG=<установить в False перед деплоем>
ALLOWED_HOSTS=<Хост, на котором будет размещен проект>
```

Создать админа для базы данных:

```
python manage.py createsuperuser
```

Создать профиль подключения к email - в файле .env нужно добавить переменные (пример для mail.ru):
```
EMAIL_MAIL=<email>
EMAIL_LOGIN_MAIL=<login>
EMAIL_PASSWORD_MAIL=<password>
```

Здесь нужно описать все остальные переменные окружения

- Командный проект [учебного курса Django](https://dvmn.org/modules/django/)
