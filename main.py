import openai
from decouple import config

openai.organization = config('OPENAI_ORGANIZATION')
openai.api_key = config('OPENAI_API_KEY')

response = openai.ChatCompletion.create(
    model='gpt-4',
    messages=[{"role": "user", "content": "Complete the test...france is known for its"}]
)

print(response.choices[0].message.content)