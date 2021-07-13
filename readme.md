## Установка

    git clone https://github.com/SaraFarron/Blog.git
    cd Blog

На Linux возможна потребуется sudo

## Использование

    docker-compose up --build

## Приложение Blog

Мини блог - после регистрации пользователь попадает в свой профиль, в котором может поменять аватар, имя, телефон и скайп.
На домашней странице отображаются все посты пользователей. Пользователь может:
1. Поменять сортировку постов
2. Создать свой пост
3. Удалить или изменить свой пост

Чужие посты редакировать нельзя.
Есть комментарии, чтобы написать один - нужно перейти на страницу поста (название поста кликабельно). Свои посты комментировать нельзя
Если пользователь попытается сделать что то, что ему делать нельзя, его просто перекинет на предыдущую страницу (обычно это домашняя страница)

## Приложение api

Позволяет получать информацию о постах в формате json или в виде html страницы. Кроме этого можно редактировать посты.

## TODO

+ Сделать подтверждение регистрации по почте
+ ДОБАВИТЬ ТЕСТЫ !!!!!!!!!!!!!!!!!!
+ Убрать говнокод, использовать миксины и прочие клевые штуки
+ Посмотреть можно ли как то расширить api
+ Добавить шифрование (lets encrypt)?
+ Выставить на heroku, github pages?
+ Подумать как приплести сюда парсинг