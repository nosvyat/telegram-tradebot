FROM python:3.11-slim

WORKDIR /app

# Копируем requirements внутрь образа
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копируем приложение
COPY ./app /app/app

# Запуск FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
