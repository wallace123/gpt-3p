import openai
from decouple import config

openai.organization = config('OPENAI_ORGANIZATION')
openai.api_key = config('OPENAI_API_KEY')

print(openai.api_key)