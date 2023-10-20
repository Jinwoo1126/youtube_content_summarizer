# youtube_content_summarizer

Author : Jinwoo Jang

## 📔 Description

This project is intended to easily summarize YouTube contents.

**The overall process is as follows:**

![Total Process](image.png)

📮 Note

Audio Segments became necessary for the following reasons:

1. whisper has `maximum content size limit (26214400)`. so, we need to reduce contents size.
2. ChatGPT's max token size is 4097(chatgpt-3.5-turbo) or 8193(chatgpt-4).



## ⌨️ Setup

1. Install dependency packages

```shell
pip install -r requirements.txt
```

2. Enter your API keys into `key.json`

```json
{
    "youtube_api":{
        "key" : "enter your youtube_api key"
    },
    "openai":{
        "key" : "enter your openai_api key",
        "organization_id" : "enter you openai's organization_id"
    }
}
```

(optional) 3. If your os OS is Windows, you need to install ffmpeg.

> Donwload url : https://ffmpeg.org/donwload.html <p> 1. click `Windows builds from gyan.dev` <p> 2. click `ffmpeg-git-full.7z` <p> 3. unzip `ffmpeg-git-full.7z` <p> 4. register `ffmpeg\\bin` on Windows Environment Variables

## 🏃‍♂️ Run Script

```shell
python main.py
```




