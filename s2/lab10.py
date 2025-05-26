import json
import re

import requests
from bs4 import BeautifulSoup

from prompts import create_answer_to_questions_accoring_to_context_test_audio_image
from utils import get_centrala_url, get_poligon_key, create_transcribe_request, create_process_image_request, \
    create_chat_request, create_payload

questions = requests.get(get_centrala_url() + '/data/' + get_poligon_key() + '/arxiv.txt').text

print(questions)
image_paths = [f"../image_files/{i}.png" for i in range(1, 7)]

audio_response = create_transcribe_request('../audio_files/rafal_dyktafon.mp3')
image_response = create_process_image_request(image_paths, 'Dokonaj opisu każdego zdjęcia po kolei, uwzględnij podpis.')

html_content = requests.get(get_centrala_url() + '/dane/arxiv-draft.html').content
soup = BeautifulSoup(html_content, "html.parser")
text_response = re.sub(r'\s*\n\s*', '\n', soup.get_text(separator="\n")).strip()

print(text_response)

messages = [
    {"role": "system", "content": create_answer_to_questions_accoring_to_context_test_audio_image(text_response + audio_response + image_response)},
    {"role": "user", "content": "O to pytania: " + questions}
]

chat_answer = create_chat_request(messages,300, "gpt-4o")

payload = create_payload("arxiv", get_poligon_key(), json.loads(chat_answer))

centrala_answer = requests.post(get_centrala_url() + '/verify', json=payload)

print(centrala_answer.text)

