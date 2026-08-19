from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="local"
)

response = client.chat.completions.create(
    model="qwen3",
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in simple terms."
        }
    ]
)

print(response.choices[0].message.content)

