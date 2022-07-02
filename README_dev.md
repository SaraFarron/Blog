## Installation

Docker is required

```
git clone https://github.com/SaraFarron/Blog.git
cd Blog
docker-compose build
```

## Использование / Usage

`docker-compose up`

If you get an ImportError rename directory Blog to blog (one in the same directory with readme)

Create superuser

`docker exec -it blog_web_1 python manage.py createsuperuser`

Enter console

`docker exec -it blog_web_1 python manage.py shell_plus`

Enter db console

`docker exec -it blog_db_1 psql -U postgres`

Run tests

`docker exec -it blog_web_1 python manage.py test`

URL:

`localhost:8000/en/`

API Docs:

`/swagger`

## TODO

#### 2021

+ Add api documentation ✅
+ Tests, CI / CD ✅
+ Use mixins and other cool stuff ✅
+ Add 404 page and get rid of all places where django tracebacks appear ✅

#### 2022

+ Moderation with admin panel ✅
+ Add users' endpoint to api ✅
+ Add a translation to various languages ✅
+ Make confirmation of registration by email ❌
+ Add the ability to respond to comments (present in the api, but in the web) ✅
+ Division into dev and production branches ✅
+ Upload to heroku, github pages, raspberry pi? ✅
+ Add rating to posts and comments
+ Add comments counter to posts
+ Add save post feature
+ Add sort by popular feature
+ Add comments history section to profile
+ Add GitHub link to navbar ✅
+ Add markdown support to posts
+ Add DMs
+ Add encryption (lets encrypt)?
+ Login / registration via cart, google account?
