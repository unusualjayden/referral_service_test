<div align="center">
  <h1>Реферральный сервис</h1>
</div>


## Использование
Для запуска проекта вам понадобится pipenv, чтобы запустить виртуальное окружение.

```shell script
pip install pipenv
```

Далее необходимо создать его и загрузить все необходимые пакеты при помощи команды:
```shell script
pipenv shell
```

Введите команду ```gunicorn referral_hammer_systems.wsgi``` для запуска прод-сервера.

Также возможно запустить дев-сервер при помощи команды ```python manage.py runserver ```