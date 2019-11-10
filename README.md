# Описание

Порт 8082.

* GET    on /storage/key-val получает запись с  ключом key-val
* POST    on /storage/key-val создат запись с  ключом key-val, в теле отправить {"message": "text" }
* DELETE on /storage/key-val удаляет запись с  ключом key-val

# Тестировани

```
curl -X POST  -H "Content-Type: application/json" -d '{"message": "Black" }' -i http://localhost:8082/storage/key-test

curl -X DELETE http://localhost:8082/storage/key-test

curl -X GET http://localhost:8082/storage/key-test

```

# Сборка

* ```docker-compose up``` запустить контейнер

