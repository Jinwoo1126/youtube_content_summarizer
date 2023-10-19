import os
import gc
from typing import Any
from pytube import YouTube
from moviepy.editor import *

from .utils import get_rfc_date

def youtube_search(youtube, q:str=None, maxResults:int=None) -> Any:
    search_response = youtube.search().list(
        q = q,
        order = "viewCount",
        publishedAfter = get_rfc_date(),
        part = "snippet",
        maxResults = maxResults
        ).execute()
    
    return search_response


def file_downloads(url:str, filename:str):
    def download(link):
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        try:
            youtubeObject.download('Downloads', filename = f"{filename}.mp4")
            return filename
        except:
            print("An error has occurred")
        print("Download is completed successfully")

    download(url)


def extract_audio(filename:str):
    video_filename = f"Downloads\{filename}.mp4"
    audio_filename = f"Downloads\{filename}.mp3"
    video = VideoFileClip(video_filename)
    video.audio.write_audiofile(audio_filename)
        
    ## gc video
    del video
    gc.collect()

    return audio_filename
