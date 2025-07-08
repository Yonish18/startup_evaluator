FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy psycopg2-binary
COPY apps/api /app/apps/api
EXPOSE 8000
