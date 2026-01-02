import requests

URL = "http://localhost:11434/api/generate"

def ask_ollama(prompt):
    payload = {
        "model": "mistral",
        "prompt": prompt
    }

    response_text = []

    with requests.post(URL, json=payload, stream=True, timeout=120) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                data = line.decode("utf-8")
                response_text.append(data)

    return "\n".join(response_text)


if __name__ == "__main__":
    print("Asking Ollama...")
    print(ask_ollama(input("Prompt: ")))
