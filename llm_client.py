import os

# 🚨 CRITICAL: Disable Streamlit-injected proxies
for k in [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "http_proxy",
    "https_proxy",
    "ALL_PROXY",
    "all_proxy",
]:
    os.environ.pop(k, None)

from groq import Groq
from config import GROQ_API_KEY

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not set in Streamlit Secrets")

client = Groq(api_key=GROQ_API_KEY)

def call_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )
    return response.choices[0].message.content
