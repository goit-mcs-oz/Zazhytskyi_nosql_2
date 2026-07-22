import os

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import torch

df = pd.read_parquet("data/arxiv_subset.parquet")

articles = (df['title'] + " [SEP] " + df['abstract']).tolist()

# Вибір пристрою
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

model  = SentenceTransformer("allenai/specter2_base", device=device)
embeddings = model.encode(articles, batch_size=64, show_progress_bar=True, normalize_embeddings=True)

print('Загальна кількість оброблених текстів', len(articles))
print('Розмірність ембеддингів', embeddings.shape)
print('Норма першого ембеддингу', np.linalg.norm(embeddings[0]))

embeddings_dir = 'embeddings'
if not os.path.isdir(embeddings_dir):
    os.makedirs(embeddings_dir)

np.save(os.path.join(embeddings_dir, 'embeddings.npy'), embeddings)