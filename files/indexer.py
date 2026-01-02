import os, faiss, pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)
file_map = []

def index_files(folder):
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            emb = model.encode(f)
            index.add([emb])
            file_map.append(path)

    pickle.dump((index, file_map), open("file_index.pkl", "wb"))

