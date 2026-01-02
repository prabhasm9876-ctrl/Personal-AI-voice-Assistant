import os
import pickle

ROOT_DIR = "D:/New folder"   # change if you want a different scope
INDEX_FILE = "file_index.pkl"

index = []
file_map = {}

for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        full_path = os.path.join(root, file)
        index.append(file.lower())
        file_map[file.lower()] = full_path

with open(INDEX_FILE, "wb") as f:
    pickle.dump((index, file_map), f)

print(f"Index created with {len(index)} files")
