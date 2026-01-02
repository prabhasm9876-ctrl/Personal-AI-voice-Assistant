import pickle
import os

INDEX_FILE = "file_index.pkl"

if not os.path.exists(INDEX_FILE):
    raise RuntimeError("File index not found. Run build_index.py first.")

index, file_map = pickle.load(open(INDEX_FILE, "rb"))

def search_file(query):
    query = query.lower()
    return [
        file_map[f] for f in index if query in f
    ]
    if not results:
        return "No files found."            
    return results