import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

INPUT_PARQUET = "data/arxiv_subset.parquet"
INPUT_EMBEDDINGS = "embeddings/embeddings.npy"
INDEX_NAME = "arxiv-papers"
VECTOR_DIM = 768
BATCH_SIZE = 200   # Pinecone рекомендує батчі до 200 векторів

# Ініціалізація клієнта
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Створюємо індекс (якщо не існує)
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=VECTOR_DIM,        # повинна збігатися з розмірністю моделі
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"  # обирайте регіон ближче до ваших користувачів
        ),
    )

index = pc.Index(INDEX_NAME)

df = pd.read_parquet(INPUT_PARQUET)
embeddings = np.load(INPUT_EMBEDDINGS)

vectors_to_upsert = []
for row in tqdm(df.itertuples(index=True), total=len(df)):
    vector_values = embeddings[row.Index].tolist() 
    id = f'paper_{str(row.Index)}'
    vectors_to_upsert.append({
        "id": id,
        "values": vector_values,
        "metadata": {
            "arxiv_id": id,
            "title": row.title,
            "abstract": row.abstract[:500],
            "authors": row.authors[:200],
            "year": row.year,
            "category": row.category
        },
    })

    if len(vectors_to_upsert) >= BATCH_SIZE:
        index.upsert(vectors=vectors_to_upsert, namespace="science-papers")
        vectors_to_upsert = []

if vectors_to_upsert:
    index.upsert(vectors=vectors_to_upsert, namespace="science-papers")
    vectors_to_upsert = []
    
stats = index.describe_index_stats()
print(f'Загальна кількість векторів в індексі: {stats["total_vector_count"]}')
    