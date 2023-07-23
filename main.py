import os
import boto3
import openai
import requests
from decouple import config

aws_access_key = config('AWS_ACCESS_KEY')
aws_secret_key = config('AWS_SECRET_KEY')
aws_location = config('AWS_LOCATION')
openai.organization = config('OPENAI_ORGANIZATION')
openai.api_key = config('OPENAI_API_KEY')

def download_audio(url, fname):
    response = requests.get(url)
    with open(fname, 'wb') as f:
        f.write(response.content)

def create_bucket(bucket_name):
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    s3_client.create_bucket(Bucket=bucket_name)
    return bucket_name

def upload_audio(fname, bucket_name):
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    s3_client.upload_file(fname, bucket_name, fname)

download_audio('https://d1le29qyzha1u4.cloudfront.net/AWS_Podcast_Episode_605.mp3', '605.mp3')
bucket_name = create_bucket('gpt3p-podcast-605')
upload_audio('605.mp3', bucket_name)
print(bucket_name)

response = openai.ChatCompletion.create(
    model='gpt-4',
    messages=[{"role": "user", "content": "Complete the test...france is known for its"}]
)

print(response.choices[0].message.content)