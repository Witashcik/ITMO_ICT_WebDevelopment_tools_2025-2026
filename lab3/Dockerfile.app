FROM python:3.12-slim

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY shared ./shared
COPY worker ./worker
COPY migrations ./migrations
COPY alembic.ini .
COPY docker/app-entrypoint.sh ./docker/app-entrypoint.sh
RUN chmod +x ./docker/app-entrypoint.sh

CMD ["./docker/app-entrypoint.sh"]
