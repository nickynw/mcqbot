FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

RUN pip install "poetry==1.4.2"

COPY . .

RUN poetry config virtualenvs.create false

RUN echo "Installing dependencies..."

RUN poetry install --no-interaction --no-ansi --verbose

ENV MODULE_NAME=app.main
ENV APP_MODULE=app.main:app
ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]