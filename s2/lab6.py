import os

import requests

from prompts import create_find_street_name_of_university
from utils import create_transcribe_request, create_chat_request, create_payload, get_poligon_key, get_centrala_url

path = "../audio_files"

transcriptions = []

for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    if os.path.isfile(file_path):
        print("Przetwarzam:", file_path)
        transcriptions.append(create_transcribe_request(file_path))

messages = [
    {"role": "system", "content": create_find_street_name_of_university(transcriptions)},
    {"role": "user", "content": "Podaj odpowiedź zgodnie z transkrypcją rozmów"}
]

response = create_chat_request(messages, 1024)

print(response)

payload = create_payload(task="mp3", apikey=get_poligon_key(), answer=response)
answer = requests.post(get_centrala_url() + "/verify", json=payload)

print(answer.text)

