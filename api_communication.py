import requests
import time


upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {"authorization": "3c6d8da6fde74785aa3e71571c482a16"}


# Set status
status_label = None


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
        return upload_response.json()["upload_url"]
    except requests.exceptions.RequestException as e:
        # global status_label
        status_label.config(text="Status: Error uploading file")
        raise RuntimeError(f"{e}")


# Transcription - Returns the ID of the Job (transcription) that is given to AssemblyAI
def transcribe(audio_url):
    transcribe_request = {"audio_url": audio_url}
    transcribe_response = requests.post(
        transcript_endpoint, json=transcribe_request, headers=headers
    )
    job_id = transcribe_response.json()["id"]
    return job_id


# Poll - Ask for whats become of the job using job id
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
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
    url = f"{transcript_endpoint}/{transcribe_id}/{file_format}"

    while True:
        data = poll(transcribe_id)
        if data["status"] == "completed":
            return requests.get(url, headers=headers)
        elif data["status"] == "error":
            return data, "[error]"
        time.sleep(4)


# ------------------------- x ------------------------- x
# a_url = upload(
#     "C:\\Users\\Muhammad Zeeshan\\Desktop\\Project\\speech-recognition\\test_files\\female's voice.wav"
# )

# print("uploading completed")
# response = get_subtitle_file(a_url, "srt")
# print(response)
# print(response.text)
