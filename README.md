Описание в файле task.md

##Инструкция к тестовому заданию

####Собрать и запустить контейнер
```
docker-compose up -d
```

####Выполнить миграции и создать пользователя
```
docker-compose exec webapp python manage.py migrate
docker-compose exec webapp python manage.py createsuperuser
```

####Запустить runserver
```
docker-compose exec webapp python manage.py runserver 0.0.0.0:8000
```

```
http://localhost:8099
```