FROM python:3.8.3-alpine

ENV BASE_DIR=/home/blog
ENV APP_USER=sara
RUN addgroup -S $APP_USER && adduser -S $APP_USER -G $APP_USER
# set work directory


RUN mkdir -p $BASE_DIR
RUN mkdir -p $BASE_DIR/static

# where the code lives
WORKDIR $BASE_DIR

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk del build-deps \
    && apk --no-cache add musl-dev linux-headers g++
# install dependencies
RUN pip install --upgrade pip
# copy project
COPY . $BASE_DIR
RUN pip install -r requirements.txt
COPY ./entrypoint.sh $BASE_DIR

CMD ["/bin/bash", "/home/blog/entrypoint.sh"]