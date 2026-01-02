import requests

url = "http://localhost:11434/api/generate"
payload = {
    "model": "mistral",
    "prompt": "Explain recursion simply",
   
}

r = requests.post(url, json=payload)
print(r.json()["response"])
