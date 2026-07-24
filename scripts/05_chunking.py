import os
import re
from typing import Callable
import numpy as np
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

def fixed_size_breakdown(text, size, overlap=0):
    words = text.split()
    chunks = []
    chunk = []
    for i, item in enumerate(words):
        if len(chunk) < size:
           chunk.append(item)
        else:
            chunks.append(' '.join(chunk))
            chunk = words[max(0,i - overlap) : i+1]

    if chunk:
        chunks.append(' '.join(chunk))

    return chunks

def semantic_chunking(text, max_words):
    sentences = [s for s in text.split('.') if s]
    chunks = []
    chunk = ''
    for item in sentences:
        if len(chunk.split()) <= max_words:
            chunk = chunk + item + '.'
        else:
            chunks.append(chunk)
            chunk = item + '.'
    
    if chunk:
        chunks.append(chunk)

    return chunks

def create_index(index_name, pc):
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=VECTOR_DIM,    
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ),
        )
    return pc.Index(index_name)

def load_to_pinecone(index, df, model, chunking_fun: Callable , chunking_params):
    vectors_to_upsert = []
    for row in tqdm(df.itertuples(index=True), total=len(df)):
        chunks = chunking_fun(row.abstract,**chunking_params)
        for i, chunk in enumerate(chunks):
            vector_values  = model.encode(chunk, batch_size=64, show_progress_bar=False, normalize_embeddings=True).tolist()
            id = f'paper_{str(row.Index)}_chunk_{i}'
            vectors_to_upsert.append({
                "id": id,
                "values": vector_values,
                "metadata": {
                    "arxiv_id": id,
                    "title": row.title,
                    "chunk_num": i,
                    "chunk": chunk,
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

def get_query_vector(query: str, model: SentenceTransformer):
    return model.encode(query, normalize_embeddings=True).tolist()

load_dotenv()

MODEL_NAME = "allenai/specter2_base"
VECTOR_DIM = 768
BATCH_SIZE = 200 
TOP_K = 5

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
model = SentenceTransformer(MODEL_NAME)
df = pd.read_parquet("data/arxiv_subset.parquet")

str_count = df['abstract'].str.len()
idxs = np.argsort(str_count)[::-1][:30].tolist()
df_top_30_articles = df.iloc[idxs]

word_count = df_top_30_articles['abstract'].str.split().apply(len)
print('Ститистика по словах')
print(word_count.describe())

index_name_chunks_fixed = "arxiv-chunks-fixed"
index_name_chunks_semantic = "arxiv-chunks-semantic"

index_chunks_fixed = create_index(index_name_chunks_fixed, pc)
index_chunks_semantic = create_index(index_name_chunks_semantic, pc)

print('\nЗавантажування Fixed-size chunking в Pinecone')
load_to_pinecone(index_chunks_fixed, df_top_30_articles, model, fixed_size_breakdown, {'size':20, 'overlap':5})
print('Завантажування Semantic chunking в Pinecone')
#load_to_pinecone(index_chunks_semantic, df_top_30_articles, model, semantic_chunking, {'max_words':70})

# Семантичний пошук

query = "teaching machines to recognize objects in pictures"
query_vector = get_query_vector(query, model)
results = index_chunks_fixed.query(namespace="science-papers", top_k=TOP_K, vector=query_vector, include_metadata=True)
print(f'\nСемантичний пошук по Fixed-size chunking:{query}')
print(f'Результати:\n')
for item in results["matches"]:
    print('title:',item['metadata']['title'])
    print('chunk:', item['metadata']['chunk'])
    print('abstract:', item['metadata']['abstract'])
    print('------------------------------')

query = "FUV-capable spectrographs"
query_vector = get_query_vector(query, model)
results = index_chunks_fixed.query(namespace="science-papers", top_k=TOP_K, vector=query_vector, include_metadata=True)
print(f'\nСемантичний пошук по Fixed-size chunking:{query}')
print(f'Результати:\n')
for item in results["matches"]:
    print('title:',item['metadata']['title'])
    print('chunk:', item['metadata']['chunk'])
    print('abstract:', item['metadata']['abstract'])
    print('------------------------------')

print('----------------------------------------------------')

query = "teaching machines to recognize objects in pictures"
query_vector = get_query_vector(query, model)
results = index_chunks_semantic.query(namespace="science-papers", top_k=TOP_K, vector=query_vector, include_metadata=True)
print(f'\nСемантичний пошук по Semantic chunking:{query}')
print(f'Результати:\n')
for item in results["matches"]:
    print('title:',item['metadata']['title'])
    print('chunk:', item['metadata']['chunk'])
    print('abstract:', item['metadata']['abstract'])
    print('------------------------------')

query = "FUV-capable spectrographs"
query_vector = get_query_vector(query, model)
results = index_chunks_semantic.query(namespace="science-papers", top_k=TOP_K, vector=query_vector, include_metadata=True)
print(f'\nСемантичний пошук по Semantic chunking:{query}')
print(f'Результати:\n')
for item in results["matches"]:
    print('title:',item['metadata']['title'])
    print('chunk:', item['metadata']['chunk'])
    print('abstract:', item['metadata']['abstract'])
    print('------------------------------')