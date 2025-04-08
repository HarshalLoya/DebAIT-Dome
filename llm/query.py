import os
import requests


def query_llm(prompt: str) -> str:
    api_key = os.getenv("GROQ_LLAMA_70B_VERSATILE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set the 'GROQ_LLAMA_70B_VERSATILE_API_KEY' environment variable."
        )

    api_url = "https://api.groq.com/openai/v1/chat/completions"    # Groq API endpoint
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "No content found in API response."
    else:
        return f"Error: {response.status_code} - {response.text}"
