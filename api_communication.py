import requests
import time
import sys
import json
from tkinter import messagebox


upload_endpoint = "https://api.assemblyai.com/v2/upload"
base_url = "https://api.assemblyai.com/v2/transcript"


global headers
headers = None
with open("keys.txt", "r") as file:
    try:
        headers = json.load(file)
    except json.decoder.JSONDecodeError as e:
        messagebox.showerror(
            "API Key Format Error", "API key must be in the dictionary format"
        )
        sys.exit(1)


# Set status
status_label = None

# Status Labels
st_label_trans = None
st_label_sub = None
st_label_summ = None


def set_status_flag(flag=None):
    global st_label_trans
    global st_label_sub
    global st_label_summ

    if flag == "transcription":
        set_status(st_label_trans)

    elif flag == "subtitle":
        set_status(st_label_sub)

    elif flag == "summary":
        set_status(st_label_summ)


def set_status(st_label):
    global status_label
    status_label = st_label


# Upload - Return the url of the uplaoded audio file
def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data  # keep returning the binary

    try:
        global status_label
        status_label.config(text="Status: Uploading...")

        upload_response = requests.post(
            upload_endpoint, headers=headers, data=read_file(filename)
        )
        return upload_response.json()["upload_url"]  # AUDIO URL IN THE CLOUD

    except requests.exceptions.RequestException as e:
        status_label.config(text="Status: Error uploading file")
        raise RuntimeError(f"{e}")


# Transcription - Returns the ID of the Job (transcription) that is given to AssemblyAI
def transcribe(audio_url, is_summarization=False):
    data = None

    if is_summarization:
        data = {
            "audio_url": audio_url,
            "summarization": True,
            "summary_model": "informative",
            "summary_type": "bullets",
        }
    elif is_summarization == False:
        data = {"audio_url": audio_url}

    transcribe_response = requests.post(base_url, json=data, headers=headers)

    job_id = transcribe_response.json()["id"]
    return job_id


# Poll - Ask for whats become of the job using job id
def poll(transcript_id):
    polling_endpoint = base_url + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


# Results - Whats the result - Completed / Processing / Error (FOR SIMPLE TRANSCRIPTION)
def get_transcription_result_url(audio_url):
    transcribe_id = transcribe(audio_url)
    while True:
        data = poll(transcribe_id)
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, "[error]"
        time.sleep(4)


# Results - Whats the result - Completed / Processing / Error (FOR SUBTITLE)
def get_subtitle_file(audio_url, file_format):
    if file_format not in ["srt", "vtt"]:
        return "Invalid file format. Valid formats are 'srt' and 'vtt'."

    transcribe_id = transcribe(audio_url)
    url = f"{base_url}/{transcribe_id}/{file_format}"

    while True:
        data = poll(transcribe_id)
        if data["status"] == "completed":
            return requests.get(url, headers=headers), None
        elif data["status"] == "error":
            return data, "[error]"
        time.sleep(4)


# Results - Whats the result - Completed / Processing / Error (FOR SUMMARIZATION)
def get_summary(audio_url):
    summary_id = transcribe(audio_url, True)
    while True:
        data = poll(summary_id)
        if data["status"] == "completed":
            return data.get("summary", ""), None
        elif data["status"] == "error":
            return data, "[error]"
        time.sleep(4)


# ------------------------- x ------------------------- x
