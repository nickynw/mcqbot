FROM python:3.9

WORKDIR /api

RUN pip install "poetry==1.4.2"

COPY ../pyproject.toml /api/pyproject.toml

COPY ../api ./api

COPY ../tests ./tests

RUN poetry config virtualenvs.create false

RUN echo "Installing dependencies..."
 
RUN  poetry install --with nx,neo4j --no-interaction --no-ansi --verbose