FROM python:3.12.2

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pg_service.conf /etc/postgresql-common/pg_service.conf

ENV PGSERVICEFILE=/etc/postgresql-common/pg_service.conf

COPY req.txt /app

RUN pip install -r req.txt

COPY . /app/

RUN python manage.py makemigrations