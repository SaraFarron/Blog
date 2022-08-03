## Description

Hi, this is a pet project that slightly got out of hand. 
It's a typical site-blog where all registered users can publish posts, 
comment, upvote/downvote and save them. The main source of inspiration is DTF.ru

## Installation

Docker is required

`git clone https://github.com/SaraFarron/Blog.git
cd Blog
docker-compose build`

## Usage

`docker-compose up`

If you get an ImportError rename folder Blog to blog (the one in the directory with readme)

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

## Currently known issues

Right now images do not upload in users' profiles because of a [bug](https://github.com/axnsan12/drf-yasg/issues/761)
with django 4.0.1 and whitenoise. As soon as I will find a solution or a fix will be released I (hopefully) will remove 
this bug. It is only present on [Heroku](https://pacific-lake-54676.herokuapp.com/en/) though, with running project 
locally (as described in README_dev.md) this problem won't appear.