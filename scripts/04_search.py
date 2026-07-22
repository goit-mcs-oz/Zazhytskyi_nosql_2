from datetime import date
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def get_query_vector(query: str, model: SentenceTransformer):
    return model.encode(query, normalize_embeddings=True).tolist()


load_dotenv()

INDEX_NAME = "arxiv-papers"
MODEL_NAME = "allenai/specter2_base"
TOP_K = 5

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(INDEX_NAME)
model = SentenceTransformer(MODEL_NAME)
df = pd.read_parquet("data/arxiv_subset.parquet")  # для отримання повного abstract

# Чистий семантичний пошук
query = "teaching machines to recognize objects in pictures"
query_vector = get_query_vector(query, model)
results = index.query(namespace="science-papers", top_k=TOP_K, vector=query_vector, include_metadata=True)

print('Чистий семантичний пошук, результати:\n')
for item in results["matches"]:
    print('title:',item['metadata']['title'])
    print('category:', item['metadata']['category'])
    print('year:', item['metadata']['year'])
    print('abstract:', item['metadata']['abstract'])
    print('------------------------------')


# Пошук з фільтрацією

query = "reinforcement learning"
# Приклад A
query_vector = get_query_vector(query, model)
results = index.query(namespace="science-papers", top_k=TOP_K, vector=query_vector, include_metadata=True,
                      filter={
                        "$and": [
                            {"category": {"$eq": "cs.LG"}},
                            {"year": {"$gte": date.today().year -5 }},
                        ]
                    },)


print('\n')
print('Пошук з фільтрацією, приклад A, результати:\n')
for item in results["matches"]:
    print('title:',item['metadata']['title'])
    print('category:', item['metadata']['category'])
    print('year:', item['metadata']['year'])
    print('abstract:', item['metadata']['abstract'])
    print('------------------------------')

# Приклад B
query_vector = get_query_vector(query, model)
results = index.query(namespace="science-papers", top_k=TOP_K, vector=query_vector, include_metadata=True,
                      filter={
                        "year": {"$lt": 2015},
                    },)


print('\n')
print('Пошук з фільтрацією, приклад B, результати:\n')
for item in results["matches"]:
    print('title:',item['metadata']['title'])
    print('category:', item['metadata']['category'])
    print('year:', item['metadata']['year'])
    print('abstract:', item['metadata']['abstract'])
    print('------------------------------')

INPUT_EMBEDDINGS = "embeddings/embeddings.npy"
embeddings = np.load(INPUT_EMBEDDINGS)

#query = "reinforcement learning"

similarity = cosine_similarity(embeddings, np.array(query_vector).reshape(1, -1)).ravel()
top5 = np.argsort(similarity)[::-1][:TOP_K]
print(f'\nTop-{TOP_K} статей для метрики cosine similarity:')
for idx in top5:
    print(f"score: {similarity[idx]:.4f}")
    print(f"title: {df.iloc[idx]['title']}, abstract: {df.iloc[idx]['abstract']}")
    print(f"abstract: {df.iloc[idx]['abstract']}")
    print('------------------------------')


dot_product = np.dot(embeddings, np.array(query_vector).reshape(1, -1).T).ravel()
top5 = np.argsort(dot_product)[::-1][:TOP_K]
print(f'\nTop-{TOP_K} статей для метрики dot product:')
for idx in top5:
    print(f"score: {similarity[idx]:.4f}")
    print(f"title: {df.iloc[idx]['title']}, abstract: {df.iloc[idx]['abstract']}")
    print(f"abstract: {df.iloc[idx]['abstract']}")
    print('------------------------------')

distance = np.linalg.norm(embeddings - np.array(query_vector).reshape(1, -1), axis=1)
top5 = np.argsort(distance)[:TOP_K]
print(f'\nTop-{TOP_K} статей для метрики L2-distance distance:')
for idx in top5:
    print(f"score: {distance[idx]:.4f}")
    print(f"title: {df.iloc[idx]['title']}, abstract: {df.iloc[idx]['abstract']}")
    print(f"abstract: {df.iloc[idx]['abstract']}")
    print('------------------------------')