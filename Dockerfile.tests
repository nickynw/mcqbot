FROM python:3.9

WORKDIR /app

RUN pip install "poetry==1.4.2"

COPY . .

RUN  poetry install --no-interaction --no-ansi