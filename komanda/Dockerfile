# Сборка для дебага
FROM python:3.10.5-alpine

# set work directory
WORKDIR /usr/src/komanda

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements/base.txt .
RUN pip install -r base.txt

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/komanda/entrypoint.sh
RUN chmod +x /usr/src/komanda/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/komanda/entrypoint.sh"]