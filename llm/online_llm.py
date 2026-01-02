def ask_llm(prompt):
    payload = {
        "model": "phi-2",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7
    }

    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json=payload,
        timeout=120
    )

    return response.json()["choices"][0]["message"]["content"]

