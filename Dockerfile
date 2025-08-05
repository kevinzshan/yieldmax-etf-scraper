FROM python:3.10-slim

WORKDIR /app

COPY app/ /app

RUN pip install --no-cache-dir requests pandas psycopg2-binary

CMD ["python", "scraper.py"]
