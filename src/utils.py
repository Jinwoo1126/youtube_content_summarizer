import os
import json
from datetime import date, timedelta
from pydub import AudioSegment


def get_config():
    # Reading keys
    json_path = "key.json"
    with open(json_path, "r") as f:
        keys = json.load(f)

    return keys


def get_rfc_date():
    # within one month
    one_month_ago = date.today() - timedelta(30)
    rfc3339_date = one_month_ago.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return rfc3339_date


def dump_file(file):
    # dump file
    with open(str(date.today().strftime('%Y-%m-%d') + '.json'), 'w') as json_file:
        json.dump(file, json_file)


def remove_files(filename):
    try:
        os.remove(f"Downloads\{filename}.mp4")
        os.remove(f"Downloads\{filename}.mp3")
    except FileNotFoundError as e:
        print(e)


def audio_segment(filename):
    AudioSegment.converter = r'C:\Users\장진우\Documents\proj\youtube_crawler\ffmpeg\ffmpeg-2023-10-18-git-e7a6bba51a-full_build\bin\ffmpeg.exe'
    AudioSegment.ffprobe = r'C:\Users\장진우\Documents\proj\youtube_crawler\ffmpeg\ffmpeg-2023-10-18-git-e7a6bba51a-full_build\bin\ffprobe.exe'

    song = AudioSegment.from_mp3(f"Downloads\{filename}.mp3")

    # PyDub handles time in milliseconds
    ten_minutes = 10 * 60 * 1000

    converted_files = []
    for cnt, idx in enumerate(range(0, len(song), ten_minutes)):
        Video_10_minutes = song[idx:idx + ten_minutes]
        converted_filename = f"Downloads\(converted)_{filename}_{cnt+1}.mp3"
        Video_10_minutes.export(converted_filename, format="mp3")
        converted_files.append(converted_filename)

    return converted_files

