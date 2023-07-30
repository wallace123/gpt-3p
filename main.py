import os
import boto3
import openai
import requests
from decouple import config

class AWSManager:
    def __init__(self, access_key, secret_key, location):
        self.s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=location)
        self.transcribe = boto3.client('transcribe', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=location)
        self.location = location

    def download_audio(self, url, fname):
        try:
            response = requests.get(url)
            with open(fname, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f'Error downloading audio: {e}')
            return False
        return True

    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
        except Exception as e:
            print(f'Error creating bucket: {e}')
            return False
        return True

    def upload_audio(self, fname, bucket_name):
        try:
            self.s3_client.upload_file(fname, bucket_name, fname)
        except Exception as e:
            print(f'Error uploading audio: {e}')
            return False
        return True

    def start_aws_transcribe(self, bucket_name, fname):
        try:
            self.transcribe.start_transcription_job(
                TranscriptionJobName=fname,
                Media={'MediaFileUri': f'https://s3.{self.location}.amazonaws.com/{bucket_name}/{fname}'},
                MediaFormat='mp3',
                LanguageCode='en-US'
            )
        except Exception as e:
            print(f'Error starting transcription job: {e}')
            return False
        return True

    def download_aws_transcribe(self, bucket_name, fname):
        transcribe = self.transcribe.get_transcription_job(TranscriptionJobName=fname)
        try:
            while transcribe['TranscriptionJob']['TranscriptionJobStatus'] == 'IN_PROGRESS':
                transcribe = self.transcribe.get_transcription_job(TranscriptionJobName=fname)
            transcribe = self.transcribe.get_transcription_job(TranscriptionJobName=fname)
        except Exception as e:
            print(f'Error downloading transcription job: {e}')
            return False
        return transcribe

class OpenAIManager:
    def __init__(self, organization, api_key):
        openai.organization = organization
        openai.api_key = api_key

    def create_chat(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f'Error creating chat: {e}')
            return None

def main():
    # Load configuration
    access_key = config('AWS_ACCESS_KEY')
    secret_key = config('AWS_SECRET_KEY')
    location = config('AWS_LOCATION')
    organization = config('OPENAI_ORGANIZATION')
    api_key = config('OPENAI_API_KEY')

    # Initialize AWS manager
    aws_manager = AWSManager(access_key, secret_key, location)

    # Download audio
    if not aws_manager.download_audio('https://d1le29qyzha1u4.cloudfront.net/AWS_Podcast_Episode_605.mp3', '605.mp3'):
        return

    # Create bucket
    if not aws_manager.create_bucket('gpt3p-podcast-605'):
        return

    # Upload audio
    if not aws_manager.upload_audio('605.mp3', 'gpt3p-podcast-605'):
        return

    # Start AWS Transcribe
    if not aws_manager.start_aws_transcribe('gpt3p-podcast-605', '605.mp3'):
        return

    if not aws_manager.download_aws_transcribe('gpt3p-podcast-605', '605.mp3'):
        return
    else:
        transcribe = aws_manager.download_aws_transcribe('gpt3p-podcast-605', '605.mp3')
        print(transcribe)

    # Initialize OpenAI manager
    openai_manager = OpenAIManager(organization, api_key)

    # Create chat
    result = openai_manager.create_chat('Complete the test...france is known for its')

    if result:
        print(result)

if __name__ == "__main__":
    main()