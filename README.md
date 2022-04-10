# Общий проект по дисциплине Базы данных


## ERD:
![alt-текст](images/ERD_v5.png "ERD")


## Текущий API:
1. /login  
   + POST		|Залогиниться  
2. /registration  
   + POST		|Зарегистрироваться  
3. /user/{id}  
   + GET		|Получить информацию о пользователе и все его фото  
   + DELETE	|Удалить пользователя и (Что-то делать с фото)  
   + PUT	|Обновить информацию о пользователе  
4. /user/{id}/album/  
   + GET?		|Получить список всех альбомов?  
   + POST		|Создать альбом  
5. /user/{id}/album/{id}  
   + GET		|Получить информацию о альбоме и все фото альбома  
   + PUT	|Изменить информацию о альбоме  
   + DELETE	|Удалить альбом  
6. /search  
   + GET		|Получить все фото удовлетворяющие параметрам  
7. /photo  
   + POST		|Загрузить фото  
8. /photo/{id}  
   + GET		|Получить полную информацию о фото  
   + DELETE	|Удалить фото  
   + PUT	|Обновить информацию о фото  
9. /photo/{id}/accessList  
   + GET		|Получить список пользователей с доступом к фото  
   + POST		|Задать список пользователей с доступом к фото
10. /photo/{id}/accessList/{user_id} 
    * DELETE	|Удалить пользователя из списка пользователей с доступом к фото
    * PUT		|Добавить пользователя в список пользователей с доступом к фото
11. /photo/{id}/comment  
    * GET???	|Получить комментарии к фото (отдельно от фото)  
    * POST		|Написать комментарий к фото  
12. /photo/{id}/comment/{id}  
    * PUT	|Изменить комментарий к фото  
    * DELETE	|Удалить комментарий к фото  
13. /theme  
    - GET		|Получить список всех тем  
    - POST		|Создать тему  
14. /theme/{id}  
    * GET???	|Получить информацию о теме? Все фото?  
    * PUT		|Изменить информацию о теме  
    * DELETE	|Удалить тему  
15. /tag  
    - GET		|Получить список всех тегов  
    - POST		|Создать новый тег  
16. /tag/{id}  
    - GET???	|Получить информацию о теге? Все фото?  
    - PUT		|Изменить информацию о теге  
    - DELETE	|Удалить тег  
17. Something else?  

## (Язык SQL DDL)

### Создание БД

Схемы будем описывать в очередности их инициализации в нашей ORM
Пояснения по работе некоторых конструкций:
* FOREIGN KEY (param1) REFERENCES table_name.param2 - назначение внешнего ключа к полю param1, по таблице table_name и полю param2 


* ON DELETE CASCADE - если в таблице table_name произошло удаление param2, то вся запись должна быть удалена из таблицы


* ON DELETE SET NULL - если в таблице table_name произошло удаление param2, то в param1 записываем значение `NULL`
  (e.g. Например, пользователь был удален, )

```sql
CREATE DATABASE gallery;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE themes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    place TEXT NOT NULL,
    description TEXT,
    private BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
);

CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    photo_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE _ (
    id SERIAL PRIMARY KEY,
    
);

CREATE TABLE _ (
    id SERIAL PRIMARY KEY,
    
);

CREATE TABLE _ (
    id SERIAL PRIMARY KEY,
    
);

CREATE TABLE _ (
    id SERIAL PRIMARY KEY,
    
);

CREATE TABLE _ (
    id SERIAL PRIMARY KEY,
    
);

```
### Наполнение БД данными