FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir fastapi uvicorn httpx openai pydantic pgvector redis asyncpg PyJWT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
