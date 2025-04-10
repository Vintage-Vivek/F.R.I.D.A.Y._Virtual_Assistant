from openai import OpenAI

client = OpenAI(
  api_key="-----------------------------",
)

completion = client.chat.completions.create(
  model="-------------------", # use model of your choice
  messages=[
    {"role": "system", "content": "You are a virtual assistant named friday skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)