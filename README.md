# Общий проект по дисциплине Базы данных
## Перед тем как работать с кодом нашего проекта
В файле `constants.py` убедитесь, что данная конфигурация может быть запущена у Вас на компьютере
(нужно указать username:password какого-либо существующего пользователя, от установленной локально PostgreSQL)

## Описание работы
Предметная область:
Web API сервиса по хранению изображений.
Пользователь может загружать на сервис свои фотографии, группировать их в альбомы,
присваивать существующие теги и темы и создавать новые.
Есть возможность контроля доступа к альбомам и конкретному изображению.

Используемые технологии:
+ Python 3.10
+ SQLAlchemy (w/ PostgreSQL)
+ flask_restx (REST_API)
+ SwaggerUI

## Entity-Relationship Diagram (ERD):
Структура  БД:  

![Entity-Relationship Diagram](images/ERD_v5.png "Entity-Relationship Diagram")


### 1. Пользователь может:
 - Загружать фото, присваивать им теги и темы
 - Создавать альбомы
 - Создавать теги
 - Удалять/Изменять свои фото/альбомы, выдавать к ним доступ другим пользователям
 - Получать доступ к (публичным или с соответствующей записью о доступе) фото 
и альбомам других пользователей
 - Писать комментарии к доступным фото

### 2. Админ может:
 - всё что может пользователь, но имеет доступ не только к своим сущностям, 
но и любого другого пользователя
 - Создавать/Удалять темы

### 3. Авторизация
В проекте используется Basic Authorization, это значит что
в заголовке каждого запроса в поле authorization должна храниться 
закодированная (base64) информация о логине и пароле ввиде:  
-H 'authorization: Basic token64'  
где token64 - это закодированная строка "login:password"  

Пример:  
curl -X 'GET' \  
    'http://localhost:5002/api/tag' \  
    -H 'accept: application/json' \  
    -H 'authorization: Basic c29tZUBtYWlsLmNvbTp6eGM='

## Swagger UI(OAS 2)
Примечание: К сожалению, у нас не работают такие атрибуты методов
как summary и deprecated, хотя в OAS 2 уже должны бы, поэтому пользоваться
Swagger UI не так удобно, как могло бы быть.

### Авторизация
Чтобы авторизоваться и не вводить закодированные логин и пароль 
в каждый запрос нужно воспользоваться штатным инструментом авторизации(пример ниже),
после чего в каждый запрос на нужные ендпоинты будет автоматически добавляться
соответствующая запись(в заголовок)  

Примечание: в это поле можно ввести любые данные, но, если пользователя
с такими данными не существует, то при требующих авторизации запросах будет
приходить ответ с кодом 401  

Пример:  
![imageAuth1](images/Auth1.png "imageAuth1")
![imageAuth2](images/Auth2.png "imageAuth2")
![imageAuth3](images/Auth3.png "imageAuth3")
![imageAuth4](images/Auth4.png "imageAuth4")

### Генерация запросов и просмотр ответов
Нажав на конкретный метод, можно увидеть его расширенную документацию:
1. Описание
2. Возможные параметры
3. Возможные коды и содержание ответов
![methodExample](images/Method1.png "method")  
![methodExample](images/Method2.png "method")  

Для того чтобы отправить запрос надо: 
1. Нажать кнопку "Try it out"
2. Ввести параметры(поля станут интерактивными)
3. Нажать кнопку "Execute"
4. Сгенерированный запрос и полученный ответ можно просмотреть ниже
![requestExample](images/RequestEx1.png "request")
![requestExample](images/RequestEx2.png "request")  
![requestExample](images/RequestEx3.png "request")

## Текущий API:
Более подробную и более читабельную документацию можно увидеть в Swagger UI
    - localhost:5002/doc

Мы старались следовать по этой Roadmap, так же здесь, подписаны те методы которые сделаны, протестированы и работают

1. /login  
   + POST		|Залогиниться-Сделано
2. /registration  
   + POST		|Зарегистрироваться-Сделано
3. /user/{id}  
   + GET		|Получить информацию о пользователе и все его фото-Сделано
   + DELETE		|Удалить пользователя и (Что-то делать с фото)-Сделано
   + PUT		|Обновить информацию о пользователе-Сделано
4. /user/{id}/album/  
   + GET		|Получить список всех альбомов-Сделано
   + POST		|Создать альбом-Сделано
5. /user/{id}/album/{id}  
   + POST		|Добавить фото в альбом-Сделано
   + GET		|Получить информацию об альбоме и все фото альбома-Сделано  
   + PUT		|Изменить информацию об альбоме-Сделано
   + DELETE		|Удалить альбом-Сделано
6. /photo
   + POST		|Загрузить фото-Сделано
8. /photo/{id}  
   + GET		|Получить полную информацию о фото-Сделано 
   + DELETE		|Удалить фото-Сделано
   + PUT		|Обновить информацию о фото-Сделано
9. /photo/{id}/accessList  
   + GET		|Получить список пользователей с доступом к фото-Сделано
10. /photo/{id}/accessList/{user_id} 
    * DELETE	|Удалить пользователя из списка пользователей с доступом к фото-Сделано
    * PUT		|Добавить пользователя в список пользователей с доступом к фото-Сделано
11. /photo/{id}/comment
    * POST		|Написать комментарий к фото-Сделано
12. /photo/{id}/comment/{id}  
    * PUT 		|Изменить комментарий к фото-Сделано
    * DELETE	|Удалить комментарий к фото-Сделано
13. /theme  
    - GET		|Получить список всех тем-Сделано
    - POST		|Создать тему-Сделано
14. /theme/{id}  
    * GET		|Получить все доступные фото с темой-Сделано
    * DELETE	|Удалить тему-Сделано
15. /tag  
    - GET		|Получить список всех тегов-Сделано
    - POST		|Создать новый тег-Сделано
16. /tag/{id}  
    - GET		|Получить все доступные фото с тегом-Сделано
    - DELETE	|Удалить тег-Сделано

## Язык SQL DDL
### Создание БД
Так как мы пользуемся средствами ORM, то мы явно не описывали все эти конструкции и не запускали, чтобы создать нашу БД,
а создаем мы нашу БД, при помощи описания полей, связей и зависимостей таблиц в ООП-формате, который при помощи ORM,
преобразуется в готовую и рабочую БД

Схемы будем описывать в очередности их инициализации в нашей ORM
Пояснения по работе некоторых конструкций:
* FOREIGN KEY (param1) REFERENCES table_name.param2 - назначение внешнего ключа 
к полю param1, по таблице table_name и полю param2


* ON DELETE CASCADE - если в таблице table_name произошло удаление
param2, то вся запись должна быть удалена из таблицы (e.g. удален пользователь -> удаляем все фотографии -> ...)


* ON DELETE SET NULL - если в таблице table_name произошло удаление param2,
то в param1 записываем значение `NULL`(e.g. удален тег/тема)

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

В связи с ограничением по времени, убрали из таблицы photos, 3 данных,
```sql
width INTEGER NOT NULL,
height INTEGER NOT NULL,
place TEXT NOT NULL
```

## SQL DML
Мы использовали ORM SQLAlchemy, поэтому чаще всего в явном виде сложные запросы 
в проекте отсутствуют, однако средствами SQLAlchemy можно конвертировать
запросы из "ORM-ного" вида в SQL.

Пример:
```Python 
public = s.query(photos).filter(
    photos.private == False,
    photos.user_id == owner_id
)
private = s.query(photos).filter(
    photos.private == True,
    photos.user_id == owner_id
)
user_access = s.query(photo_access).filter(
    photo_access.user_id == viewer_id
)

private_with_acc = private.join(user_access)
```
```SQL
print(private_with_acc)

SELECT photos.id AS photos_id, photos.user_id AS photos_user_id, photos.url AS photos_url, photos.description AS photos_description, photos.private AS photos_private, photos.created_at AS photos_created_at 
FROM photos JOIN (SELECT photo_access.id AS photo_access_id, photo_access.photo_id AS photo_access_photo_id, photo_access.user_id AS photo_access_user_id 
FROM photo_access 
WHERE photo_access.user_id = %(user_id_1)s) AS anon_1 ON photos.id = anon_1.photo_access_photo_id 
WHERE photos.private = true AND photos.user_id = %(user_id_2)s
```

### Наполнение БД данными (и генерация)
В файле `generator.py`  запустив `if __name__ == "__main__":`, можно сгенерировать данные для работы с БД, 
также постарались сделать хоть каким-то образом читаемый вывод из таблиц.


## Взаимодействие с ORM
Общая структура работы SQLAlchemy 
![Architecture of SQLA](images/sqla_engine_arch.png "Architecture of SQLA")
`Engine` ссылается как на `Dialect`, так и на `Pool`, которые вместе
интерпретируют функции модуля `DBAPI`, а также поведение БД.

### Термины для работы с ORM
* ORM (Object-Relational Mapping) - инструмент, предоставляющий возможность 
создавать, связывать (описывать отношения) в БД, при помощи средств ООП.
Позволяет нам создать виртуальную объектную базу данных, которую преобразует 
* в выбранную нами БД.\
Также включает в себя модули проверки взаимодействия: 
    * с БД (и ее диалектом),
    * с DBAPI
    * и другие...


* Engine (движок) - базовая ('отправная') точка для приложений SQLAlchemy, 
ссылается на фактическую БД и ее DBAPI, доставляемая приложению SQLALchemy через
пул соединений и диалект, 
который описывает, как обращаться к особому виду комбинации DB/DBAPI. \
По реализации - это фабрика, которая может создавать для нас новые подключения
к БД.\
Обладает параметрами при инициализации: 
  * echo -
  * pool_size -
  * max_overflow -
  * poolclass -
  * pool_pre_ping -
  * и другие
  
а также свойствами например такими как - поддержка соединения внутри пула 
соединений для быстрого повторного использования и др.


* Driver - DBAPI, которая будет использована, чтобы подключиться к БД


* Session - сессия


### Взаимодействия с БД, через ORM
#### Взаимодействие с Session()
Есть несколько способов взаимодействия с DB при помощи SQLAlchemy, мы
воспользуемся одним из них:\
При помощи использования `sqlalchemy.orm.sessionmaker()` - предоставляет 
фабрику объектов Session, 
с фиксированной конфигурацией (например с заданным `Engine`). Так как 
Session будет иметь объект `Engine`,
`sessionmaker()` позволяет получить доступ (сессию) к движку, который был 
предоставлен ранее.

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

Чтобы, выполнить запрос к Базе Данных, через ORM, можно воспользоваться двумя видами обращений:
* INSERT INTO users (full_name, email, password)\
  VALUES ('{full_name}', '{email}', '{password}')

* Session().add(users(full_name, email, password))


## Эксперимент с кэшированием
Кэширование выполняется для каждого оператора путем создания ключа кэша, который представляет структуру оператора, а затем генерации строки SQL для текущего диалекта, только если этот ключ отсутствует в кэше. Все операторы поддерживают кэширование, однако некоторые функции, такие как INSERT с большим набором параметров, намеренно обходят кэширование. Ведение журнала SQL покажет статистику для каждого оператора, независимо от того, были ли они извлечены из кэша.

В SQLAlchemy при инициализации таблицы (ее создании, в том числе) мы добавили дополнительный параметр - 
query_cache_size - который отвечает за размер кэша, используемого для кэширования строковой формы запросов SQL. 

Этот параметр должен быть установлен в ноль, чтобы отключить кэширование.

Кэш очищается от наименее использовавшихся элементов, когда его размер достигает N * 1,5. По умолчанию установлено значение 500, что означает, что кэш всегда будет хранить не менее 500 операторов SQL при заполнении и будет увеличиваться до 750 элементов, после чего он укорачивается обратно до 500 путем удаления 250 наименее использовавшихся элементов.

Тест проводился на следующем размере данных:
* 100 пользователей
* 5 тысяч фотографий
* и остальные данные не больше 100 для каждого пользователя 

Проверим время выполнения достаточно сложного запроса к БД с кэшированием и без.

![test](images/performance_test.png)

Как видим, скорость выполнения этого запроса с кэшированием кратно выше, чем без кэширования 

## Выводы
В ходе работы:

    + использовали многие возможности реляционных баз данных  
    + Познакомились с ORM SQLAlchemy
    + Научились инициализировать базу данных, создавать связанные таблицы
    + Научились заполнять базу данных автоматически генерируемыми данными
    + Использовали сложные и вложенные запросы
    + Попробовали парное программирование
    + создали RESTful web сервис с использованием Python(Flask)
