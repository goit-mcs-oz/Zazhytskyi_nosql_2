import os

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

df = pd.read_parquet("data/arxiv_subset.parquet")

articles = (df['title'] + " [SEP] " + df['abstract']).tolist()

model  = SentenceTransformer("allenai/specter2_base")
embeddings = model.encode(articles, batch_size=64, show_progress_bar=True, normalize_embeddings=True)

print('загальну кількість оброблених текстів', len(articles))
print('розмірність ембеддингів', embeddings.shape)
print('норму першого ембеддингу', np.linalg.norm(embeddings[0]))

embeddings_dir = 'embeddings'
if not os.path.isdir(embeddings_dir):
    os.makedirs(embeddings_dir)

np.save(os.path.join(embeddings_dir, 'embeddings.npy'), embeddings)