FROM python:3.9-slim-buster

WORKDIR /frontend

RUN pip install "poetry==1.4.2"

COPY ../pyproject.toml /frontend/pyproject.toml

COPY ../frontend ./frontend

RUN poetry config virtualenvs.create false

RUN echo "Installing dependencies..."

RUN poetry install --with nx,frontend --no-interaction --no-ansi --verbose

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=frontend/app.py

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]