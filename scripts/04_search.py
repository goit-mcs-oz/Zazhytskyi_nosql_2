from datetime import date
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

def get_query_vector(query: str, model: SentenceTransformer):
    return model.encode(query).tolist()


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

# Приклад A
query = "reinforcement learning"
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
query = "reinforcement learning"
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
