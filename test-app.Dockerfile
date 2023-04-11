FROM python:3.9

WORKDIR /app

RUN pip install "poetry==1.4.2"

COPY . .

RUN poetry config virtualenvs.create false
 

RUN  poetry install  --with "code_audit" --no-interaction --no-ansi --verbose