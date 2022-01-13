#### Этот проект постоянно обновляется / This project is constantly updating 

Планируется разделение на dev и prod версию, добавление шифрования, тестов, CI/CD, генерируемой документации,
и будут добавляться фичи (добавление модерации, статистики просмотра и комментирования постов)


It is planned to split this website into dev and prod versions, add encryption, tests, CI/CD, generate docs,
and some features will be added  (add moderation, posts' and comments' stats)

## Установка / Installation

Требуется докер / Docker is required

    git clone https://github.com/SaraFarron/Blog.git
    cd Blog

Переименовать tmp.env в .env / Rename tmp.env to .env

    docker-compose build

## Использование / Usage

    docker-compose up

Если вылетает ImportError переименуйте папку Blog в blog (которая лежит в одной директории с readme)

If you get an ImportError rename directory Blog to blog (one in the same directory with readme)

Создать суперпользователя / Create superuser

    docker exec -it blog_web_1 python manage.py createsuperuser

Войти в консоль / Enter console

    docker exec -it blog_web_1 python manage.py shell_plus

## Описание / Description

Сайт мини-блог. При первом посещении пользователю требуется зарегистрироваться, при регистрации его отправляет
на страницу профиля, где он может изменить что-то и увидеть свой api токен для авторизации запросов.
Пользователи могут создавать статьи, менять их, удалять, а также оставлять комментарии. Изменять и удалять
можно только свои статьи. API повторяет весь функционал.

Mini-blog site. On the first visit, the user needs to register, upon registration it is sent
to the profile page, where he can change something and see his api token for authorizing requests.
Users can create articles, change them, delete them, and also leave comments. Modify and delete
you can only your own articles. API repeats all functionality. 

## TODO

#### 2021

+ Добавить документацию api / Add api documentation ✅
+ Тесты, CI/CD / Tests, CI / CD ✅❌
+ Использовать миксины и прочие клевые штуки / Use mixins and other cool stuff ✅
+ Добавить страницу 404, убрать все места где вылетают трейсбеки джанго / Add 404 page and get rid of all places where django tracebacks appear ✅

#### 2022

+ Модерация с админ панелью / Moderation with admin panel ✅
+ Добавить эндпоинт с пользователями в api / Add users' endpoint to api ✅
+ Добавить перевод на разные языки / Add a translation to various languages ✅
+ Сделать подтверждение регистрации по почте / Make confirmation of registration by email ❌
+ Добавить возможность отвечать на комментарии (в api есть, в вебе нет) / Add the ability to respond to comments (present in the api, but in the web)
+ Вход/регистрация через телегу, аккаунт гугл? / Login / registration via cart, google account?
+ Добавить шифрование (lets encrypt)? / Add encryption (lets encrypt)?
+ Выставить на heroku, github pages, raspberry pi? / Upload to heroku, github pages, raspberry pi?
+ Добавить фронт на js:  Add front on js:
  + сделать бекенд как обычное api и обмениваться jsonом с фронтом / make the backend like a simple api and exchange json with the front 
