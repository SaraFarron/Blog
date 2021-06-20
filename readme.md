## Установка

    git clone https://github.com/SaraFarron/Blog.git
    cd Blog
    docker-compose build .

На Linux возможна потребуется sudo

## Использование

    docker-compose up

При запуске и переходе на 'localhost:port' (по умолчанию 127.0.0.1:8000) сайт встречает ошибкой. Пока что я специально оставил эту ошибку - в ней сразу показывается какие есть адреса url.
При добавлении упомянутых в ошибке /blog, /api, /admin в адресную строку попадаем в блог, api и админку соответственно. Если прописать /images/[имя изображения], то откроется изображение в браузере. Не считая аватаров, там пока ничего нет.

Все написано на английском (кроме тестовых названий объектов, которые придумывались наобум), так как киррилица в файлах с кодом выглядела как то неестественно. ~~Автор ни в коем случае не хотел подчеркнуть знания английского чуть выше среднего статистического россиянина~~ Возможно в дальнейшем появится перевод на русский. Общий дизайн был по большей части взят [от сюда](https://dtf.ru/new) и свободных библиотек вроде Bootstrap. Автор в первую очередь ставит цель развития навыков backend разработки и знает инструменты frontend лишь на базовом уровне. ~~Хотя подозревает, что знание sql и django тоже далеко от этого уровня не ушло.~~

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
