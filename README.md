### Описание / Description

Сайт-блог, мой клон [DTF](www.dtf.ru) который я нагло копирую для своего развития как backend веб разработчика.
Моя цель реализовать большую часть функционала бэкенд части DTF возможно с добавлением каких-либо своих особенностей.
Фронт-энд и веб дизайн меня интересуют в меньшей части, поэтому внешний вид оставляет желать лучшего, а JS нет вообще.

Blog-site, my clone of [DTF](www.dtf.ru), which I impudently copy for my personal growth in backend web development.
My goal is to make most of DTF's backend functionality, maybe with my own features.
I am not interested as much in frontend, that's why looks of website are not that great and JS is not present at all.

### Текущие известные проблемы / Currently known issues

Сейчас на сайте не загружаются аватары в профиле пользователя из-за [бага](https://github.com/axnsan12/drf-yasg/issues/761)
django 4.0.1 и whitenoise. Как только я найду решение проблемы или фикс будет выпущен я (надеюсь) уберу этот баг.
Проблема присутствует только на [Heroku](https://pacific-lake-54676.herokuapp.com/en/), если запускать локально
(как описано в README_dev.md) - проблема отсутствует

Right now images do not upload in users' profiles because of a [bug](https://github.com/axnsan12/drf-yasg/issues/761)
with django 4.0.1 and whitenoise. As soon as I will find a solution or a fix will be released I (hopefully) will remove 
this bug. It is only present on [Heroku](https://pacific-lake-54676.herokuapp.com/en/) though, with running project 
locally (as described in README_dev.md) this problem won't appear.

Если поставить дефолтную аватарку то вылетает 500 / Default avatar button creates 500
