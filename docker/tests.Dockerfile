FROM python:3.9

WORKDIR /app

RUN pip install "poetry==1.4.2"

COPY ../pyproject.toml /app/pyproject.toml

COPY ../app ./app

COPY ../tests ./tests

RUN poetry config virtualenvs.create false

RUN echo "Installing dependencies..."
 
RUN  poetry install --with nx,neo4j --no-interaction --no-ansi --verbose