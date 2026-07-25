import os
import math
from typing import List, Tuple
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

def reciprocal_rank_fusion(
    rankings: List[List[int]],
    k: int = 60
) -> List[Tuple[int, float]]:
    """
    Об'єднує кілька ранжованих списків через RRF.
    """
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def BM25_search(query:str, bm25: BM25Okapi) -> List[int]:
    bm25_scores = bm25.get_scores(query.lower().split())
    return list(np.argsort(bm25_scores)[::-1])

def vector_search(query:str, model: SentenceTransformer, corpus:List[str])-> List[int]:
    corpus_embeddings = model.encode(corpus, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
    query_embeddings = model.encode(query, normalize_embeddings=True)
    scores = np.dot(corpus_embeddings, query_embeddings)

    return list(np.argsort(scores)[::-1])

def hybrid_search(query:str,  bm25: BM25Okapi, model: SentenceTransformer, corpus:List[str]) -> List[Tuple[str, float]]:
    bm25_ranking = BM25_search(query, bm25)
    vector_ranking = vector_search(query, model, corpus)
    fused = reciprocal_rank_fusion([bm25_ranking, vector_ranking])[:5]

    return [(corpus[id], score) for id, score in fused]

load_dotenv()

INDEX_NAME = "arxiv-papers"
MODEL_NAME = "allenai/specter2_base"
TOP_K = 10   # беремо ширше, щоб RRF міг переранжувати

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(INDEX_NAME)
model = SentenceTransformer(MODEL_NAME)
df = pd.read_parquet("data/arxiv_subset.parquet").reset_index(drop=True)

corpus = (df["title"] + " [SEP] "  + df["abstract"]).tolist()

bm25 = BM25Okapi([item.lower().split() for item in corpus])

# ----------------------------------------------------------

# Запит точний термін ("BERT fine-tuning")
query = "BERT fine-tuning"

print('\n'); 

bm25_ranking = BM25_search(query, bm25)
print(f'Результати пошуку за BM25 за запитом: {query}:')
for idx in bm25_ranking[:5]:
    print(f" - {corpus[idx]}")

print('\n');   

vector_ranking = vector_search(query, model, corpus)
print(f'Результати векторного пошуку за запитом: {query}:')
for idx in vector_ranking[:5]:
    print(f" - {corpus[idx]}")

print('\n');   

results = hybrid_search(query,  bm25, model, corpus)
print(f'Результати гібридного пошуку з RRF за запитом: {query}:')
for doc, score in results[:5]:
    print(f" - RRF={score:.4f} {doc}")

print("///////////////////////////////////////////////////////////")

# Запит ім’я автора ("Yann LeCun convolutional networks")
query = "Yann LeCun convolutional networks"

print('\n'); 

bm25_ranking = BM25_search(query, bm25)
print(f'Результати пошуку за BM25 за запитом: {query}:')
for idx in bm25_ranking[:5]:
    print(f" - {corpus[idx]}")

print('\n');   

vector_ranking = vector_search(query, model, corpus)
print(f'Результати векторного пошуку за запитом: {query}:')
for idx in vector_ranking[:5]:
    print(f" - {corpus[idx]}")

print('\n');   

results = hybrid_search(query,  bm25, model, corpus)
print(f'Результати гібридного пошуку з RRF за запитом: {query}:')
for doc, score in results[:5]:
    print(f" - RRF={score:.4f} {doc}")

print("///////////////////////////////////////////////////////////")

# Запит перефразування без явних термінів("making computers understand human emotions from text")
query = "making computers understand human emotions from text"

print('\n'); 

bm25_ranking = BM25_search(query, bm25)
print(f'Результати пошуку за BM25 за запитом: {query}:')
for idx in bm25_ranking[:5]:
    print(f" - {corpus[idx]}")

print('\n');   

vector_ranking = vector_search(query, model, corpus)
print(f'Результати векторного пошуку за запитом: {query}:')
for idx in vector_ranking[:5]:
    print(f" - {corpus[idx]}")

print('\n');   

results = hybrid_search(query,  bm25, model, corpus)
print(f'Результати гібридного пошуку з RRF за запитом: {query}:')
for doc, score in results[:5]:
    print(f" - RRF={score:.4f} {doc}")