# from groq import Groq
# from config import GROQ_API_KEY

# client = Groq(api_key=GROQ_API_KEY)

# def call_llm(system_prompt, user_prompt):
#     try:
#         response = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             temperature=0.2
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"LLM Error: {str(e)}"
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def call_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
