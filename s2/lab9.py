import json

import requests

from prompts import create_extract_text_from_image_prompt, create_categorize_text_prompt
from utils import read_file_content, create_generate_image_request, create_process_image_request, \
    create_transcribe_request, create_chat_request, create_payload, get_poligon_key, get_centrala_url

data_map = {}

text_files = [
    '../text_files/2024-11-12_report-00-sektor_C4.txt',
    '../text_files/2024-11-12_report-01-sektor_A1.txt',
    '../text_files/2024-11-12_report-02-sektor_A3.txt',
    '../text_files/2024-11-12_report-03-sektor_A3.txt',
    '../text_files/2024-11-12_report-04-sektor_B2.txt',
    '../text_files/2024-11-12_report-05-sektor_C1.txt',
    '../text_files/2024-11-12_report-06-sektor_C2.txt',
    '../text_files/2024-11-12_report-07-sektor_C4.txt',
    '../text_files/2024-11-12_report-08-sektor_A1.txt',
    '../text_files/2024-11-12_report-09-sektor_C2.txt',
]

image_files = [
    '../image_files/2024-11-12_report-13.png',
    '../image_files/2024-11-12_report-14.png',
    '../image_files/2024-11-12_report-15.png',
    '../image_files/2024-11-12_report-16.png',
    '../image_files/2024-11-12_report-17.png'
]

audio_files = [
    '../audio_files/2024-11-12_report-10-sektor-C1.mp3',
    '../audio_files/2024-11-12_report-11-sektor-C2.mp3',
    '../audio_files/2024-11-12_report-12-sektor_A1.mp3',
]

for text_file_path in text_files:
    data_map[text_file_path.split('/')[-1]] = read_file_content(text_file_path)

print(data_map)

for image_file_path in image_files:
    data_map[image_file_path.split('/')[-1]] = create_process_image_request([image_file_path], create_extract_text_from_image_prompt())

print(data_map)

for audio_file_path in audio_files:
    data_map[audio_file_path.split('/')[-1]] = create_transcribe_request(audio_file_path)

print(data_map)

messages = [
    {"role": "system", "content": create_categorize_text_prompt()},
    {"role": "user", "content": "O to dane w formacie mapy: " + json.dumps(data_map) + ". Podaj odpowiedź"}
]

answer = json.loads(create_chat_request(messages, 200))
print(answer)

answer_json = {
    "people": answer['people'],
    "hardware": answer['hardware']
}

payload = create_payload('kategorie', get_poligon_key(), answer)

response = requests.post(get_centrala_url() + '/verify', json=payload)

print(response.text)