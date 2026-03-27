import os
import requests
 
# Prefer environment variable over hardcoding
API_KEY = os.environ.get("GROQ_API_KEY", "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")
 
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
 
 
def call_llm(prompt: str, system: str = None) -> str:
    """
    Call Groq LLM (Llama 3.1 8B Instant)
    Supports optional system prompt like Gemini version
    """
 
    messages = []
 
    # Optional system instruction (to match your previous design)
    if system:
        messages.append({"role": "system", "content": system})
 
    messages.append({"role": "user", "content": prompt})
 
    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.3   # better for structured outputs
        }
    )
 
    if response.status_code != 200:
        print("Groq API Error:", response.text)
        raise Exception(f"Groq API Error: {response.text}")
 
    data = response.json()
 
    if "choices" not in data or not data["choices"]:
        raise Exception("No response from Groq LLM")
 
    return data["choices"][0]["message"]["content"]
