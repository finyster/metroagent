import os
from pgvector.asyncpg import AsyncPGVector, openai_embeddings

PG_DSN = os.getenv('PG_DSN', 'postgresql://user:pass@localhost:5432/db')

vector_store = AsyncPGVector.from_dsn(PG_DSN, embedding_function=openai_embeddings)
