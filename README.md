# Общий проект по дисциплине Базы данных


## Entity-Relationship Diagram (ERD):
![Entity-Relationship Diagram](images/ERD_v5.png "Entity-Relationship Diagram")


## Текущий API:
1. /login  
   + POST		|Залогиниться-Сделано
2. /registration  
   + POST		|Зарегистрироваться-Сделано
3. /user/{id}  
   + GET		|Получить информацию о пользователе и все его фото-Сделано
   + DELETE		|Удалить пользователя и (Что-то делать с фото)-
   + PUT		|Обновить информацию о пользователе-Сделано
4. /user/{id}/album/  
   + GET?		|Получить список всех альбомов?-
   + POST		|Создать альбом-Сделано
5. /user/{id}/album/{id}  
   + POST		|Добавить фото в альбом-Сделано
   + GET		|Получить информацию о альбоме и все фото альбома-  
   + PUT		|Изменить информацию о альбоме-
   + DELETE		|Удалить альбом-
7. /search  
   + GET		|Получить все фото удовлетворяющие параметрам-
8. /photo  
   + POST		|Загрузить фото-Сделано
9. /photo/{id}  
   + GET		|Получить полную информацию о фото- 
   + DELETE	|Удалить фото-
   + PUT	|Обновить информацию о фото- 
10. /photo/{id}/accessList  
    + GET		|Получить список пользователей с доступом к фото-Сделано
11. /photo/{id}/accessList/{user_id} 
    * DELETE	|Удалить пользователя из списка пользователей с доступом к фото-Сделано
    * PUT		|Добавить пользователя в список пользователей с доступом к фото-Сделано
12. /photo/{id}/comment  
    * GET???	|Получить комментарии к фото (отдельно от фото)-
    * POST		|Написать комментарий к фото -Сделано
13. /photo/{id}/comment/{id}  
    * PUT 		|Изменить комментарий к фото-
    * DELETE	|Удалить комментарий к фото- 
14. /theme  
    - GET		|Получить список всех тем+-
    - POST		|Создать тему-Сделано
15. /theme/{id}  
    * GET???	|Получить информацию о теме? Все фото?-
    * PUT		|Изменить информацию о теме-
    * DELETE	|Удалить тему+-
16. /tag  
    - GET		|Получить список всех тегов+-
    - POST		|Создать новый тег-Сделано
17. /tag/{id}  
    - GET???	|Получить информацию о теге? Все фото?-
    - PUT		|Изменить информацию о теге-
    - DELETE	|Удалить тег-
18. Something else?  

## (Язык SQL DDL)

### Создание БД

Схемы будем описывать в очередности их инициализации в нашей ORM
Пояснения по работе некоторых конструкций:
* FOREIGN KEY (param1) REFERENCES table_name.param2 - назначение внешнего ключа к полю param1, по таблице table_name и полю param2 


* ON DELETE CASCADE - если в таблице table_name произошло удаление param2, то вся запись должна быть удалена из таблицы


* ON DELETE SET NULL - если в таблице table_name произошло удаление param2, то в param1 записываем значение `NULL`
  (e.g. пользователь был удален, )

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
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE photo_themes (
    id SERIAL PRIMARY KEY,
    photo_id INTEGER NOT NULL,
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE,
    theme_id INTEGER NOT NULL,
    FOREIGN KEY (theme_id) REFERENCES themes(id) ON DELETE CASCADE,
);

CREATE TABLE photo_tags (
    id SERIAL PRIMARY KEY,
    photo_id INTEGER NOT NULL,
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE photo_access (
    id SERIAL PRIMARY KEY,
    photo_id INTEGER NOT NULL,
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE album_photos (
    id SERIAL PRIMARY KEY,
    photo_id INTEGER NOT NULL,
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE,
    album_id INTEGER NOT NULL,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE
);

CREATE TABLE album_access (
    id SERIAL PRIMARY KEY,
    album_id INTEGER NOT NULL,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```
### Наполнение БД данными


## Взаимодействие с ORM
Общая структура работы SQLAlchemy 
![Architecture of SQLA](images/sqla_engine_arch.png "Architecture of SQLA")
`Engine` ссылается как на `Dialect`, так и на `Pool`, которые вместе интерпретируют функции модуля `DBAPI`, а также поведение БД.

### Термины для работы с ORM
* ORM (Object-Relational Mapping) - инструмент, предоставляющий возможность 
создавать, связывать (описывать отношения) в БД, при помощи средств ООП.
Позволяет нам создать виртуальную объектную базу данных, которую преобразует в выбранную нами БД.\
Также включает в себя модули проверки взаимодействия: 
    * с БД (и ее диалектом),
    * с DBAPI
    * и другие...


* Engine (движок) - базовая ('отправная') точка для приложений SQLAlchemy, 
ссылается на фактическую БД и ее DBAPI, доставляемая приложению SQLALchemy через пул соединений и диалект, 
который описывает, как обращаться к особому виду комбинации DB/DBAPI. \
По реализации - это фабрика, которая может создавать для нас новые подключения к БД.\
Обладает параметрами при инициализации, 
  * привет \
a
а также свойствами например такими как, 
    * поддержка соединения внутри пула соединений для быстрого повторного использования


* Driver - DBAPI, которая будет использована, чтобы подключиться к БД


* Session - сессия


### Взаимодействия с БД, через ORM
#### Взаимодействие с Session()
Есть несколько способов взаимодействия с DB при помощи SQLAlchemy, мы воспользуемся одним из них:\
При помощи использования `sqlalchemy.orm.sessionmaker()` - предоставляет фабрику объектов Session, 
с фиксированной конфигурацией (например с заданным `Engine`). Так как Session будет иметь объект `Engine`,
`sessionmaker()` позволяет получить доступ (сессию) к движку, который был предоставлен ранее.

```python
# Объявление двух объектов, 
# Базы - для реализации таблиц
Base = declarative_base()
# Сессии - для взаимодействия с БД
Session = sessionmaker()

# Создание движка, по ссылке и др. параметрами
engine = create_engine(url=db, echo=False, pool_size=10, max_overflow=0, poolclass=QueuePool, pool_pre_ping=True)

# Подключение к базе данных
Session.configure(bind=engine)

# если БД, по указанному адресу, не существует, то создаем ее
if not database_exists(engine.url):
    create_database(engine.url)

# Инициализация БД, по таблицам (и их свойствам), созданных унаследованными от Base
Base.metadata.create_all(engine)
```
#### Взаимодействие с БД, при помощи Session()

Чтобы, выполнить запрос к Базе Данных, через ORM, можно воспользоваться тремя видами обращений:
* INSERT INTO users (full_name, email, password)\
  VALUES ('{full_name}', '{email}', '{password}')

* Session().add(users(full_name, email, password))


