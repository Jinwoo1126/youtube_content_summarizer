import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import openai

from src.utils import get_config, dump_file, remove_files, audio_segment
from src.youtube_fn import youtube_search, file_downloads, extract_audio


if __name__ == "__main__":
    keys = get_config()

    openai.organization = keys["openai"]["organization_id"]
    openai.api_key = keys["openai"]["key"]

    DEVELOPER_KEY = keys["youtube_api"]["key"] 
    YOUTUBE_API_SERVICE_NAME="youtube"
    YOUTUBE_API_VERSION="v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube_search(youtube, q="이차전지", maxResults=1)
    
    os.makedirs(os.path.join(os.getcwd(), 'Downloads'), exist_ok=True)

    for item in search_response['items']:
        video_url = 'http://www.youtube.com/watch?v=' + item['id']['videoId']
        filename = item['id']['videoId']

        file_downloads(video_url, filename)
        audio_filename = extract_audio(filename)

        converted_files = audio_segment(filename)
        remove_files(filename)

        item['summary'] = []

        for idx, file in enumerate(converted_files):
            audio_file = open(file, "rb")

            ## STT with whisper
            print("Calling trascribe from whisper...")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            text = transcript["text"]
            print(len(text), text)

            ## Text Summarization with chatGPT
            print("Calling chatGPT...")
            response= openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."},
                    {"role": "user", "content": f"Summarize the following text: {text[:4096]}"}
                ]
            )

            print(response['choices'][0]['message']['content'])

            item['summary'].append(response['choices'][0]['message']['content'])

    dump_file(search_response)