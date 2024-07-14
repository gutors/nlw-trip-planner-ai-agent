from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Vou viajar para Asia em Agosto de 2024. Qual o melhor destino?"},
  ]
)

print(response.choices[0].message.content)