FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Comando para ejecutar el worker
CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]