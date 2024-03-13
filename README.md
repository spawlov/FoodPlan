# Подбор здорового питания
Сайт по подбору питания на каждый день.

### Как запустить:

- Скачать или склонировать [репозиторий](https://github.com/Ash2803/foodplan)
- У вас должен быть установлен Python 3.9 или выше;
- Создать виртуальное окружение:

```commandline
python3 -m venv venv
```
- Установить зависимости:
```commandline
pip install -r requirements.txt
```
Создать файл `.env` и задать переменные окружения:
```
`SECRET_KEY`=<Здесь должен быть секретный ключ Django>
`DEBUG`=<установить в False перед деплоем>
`ALLOWED_HOSTS`=<Хост, на котором будет размещен проект>
`EMAIL_MAIL`=<мейл от адреса которого будет рассылка писем>
`EMAIL_LOGIN_MAIL`=<мейл от адреса которого будет рассылка писем>
`EMAIL_PASSWORD_MAIL`=<пароль мейла>
```
Затем проведите миграции, командой `migrate` :
```commandline
python manage.py migrate
```
- Создайте админка:
```commandline
python manage.py createsuperuser
```
- Запустите сервер:
```commandline
python manage.py runserver
```
- Командный проект [учебного курса Django](https://dvmn.org/modules/django/)
