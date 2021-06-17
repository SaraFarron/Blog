#FROM python:3
#
#COPY . .
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#
#ENTRYPOINT [ "python", "manage.py" ]
#CMD [ "runserver", "0.0.0.0:8000" ]

FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/