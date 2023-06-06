FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /api

RUN pip install "poetry==1.4.2"

COPY ../pyproject.toml /api/pyproject.toml

COPY ../api ./api

RUN poetry config virtualenvs.create false

RUN echo "Installing dependencies..."

RUN poetry install --with nx,api --no-interaction --no-ansi --verbose

ENV MODULE_NAME=api.main
ENV APP_MODULE=api.main:api

CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "80"]