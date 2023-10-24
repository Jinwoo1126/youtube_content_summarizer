import os
import gc
from typing import Any
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import *

from .utils import get_rfc_date

def query_search(youtube, q:str=None, maxResults:int=None) -> Any:
    search_response = youtube.search().list(
        q = q,
        order = "viewCount",
        publishedAfter = get_rfc_date(),
        part = "snippet",
        maxResults = maxResults
        ).execute()
    
    return search_response


def channel_search(youtube, channel_id:str=None) -> Any:
    search_response = youtube.search().list(
        channelId = channel_id,
        order = "viewCount",
        publishedAfter = get_rfc_date(),
        part = "snippet"
        ).execute()
    
    return search_response


def get_caption(url:str, filename:str):    
    # assigning srt variable with the list 
    # of dictionaries obtained by the get_transcript() function
    srt = YouTubeTranscriptApi.get_transcript(filename, languages=['ko'])
    
    # return the result
    return srt


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
    video_filename = os.path.join("Downloads", f"{filename}.mp4")
    audio_filename = os.path.join("Downloads", f"{filename}.mp3")
    video = VideoFileClip(video_filename)
    video.audio.write_audiofile(audio_filename)
        
    ## gc video
    del video
    gc.collect()

    return audio_filename
