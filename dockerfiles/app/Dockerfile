# syntax=docker/dockerfile:1

FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . .
RUN apk update \
    && apk add netcat-openbsd postgresql-dev gcc python3-dev musl-dev \
    && pip install -r requirements.txt
COPY /dockerfiles/app/entrypoint.sh .
COPY . .
ENTRYPOINT ["/code/entrypoint.sh"]