import json

import requests

from chat_request import get_poligon_key, get_centrala_url, create_chat_request
from prompts import create_give_answers_to_question


def split_text_by_length(text, max_chars=3000):
    chunks = []
    current = ""

    for line in text.splitlines(keepends=True):
        if len(current) + len(line) > max_chars:
            chunks.append(current)
            current = ""
        current += line

    if current:
        chunks.append(current)

    return chunks


data = requests.get(get_centrala_url() + "/data/" + get_poligon_key() + "/json.txt").text
data_json = json.loads(data)
# print(data_json)

for element in data_json['test-data']:
    if 'test' in element and element['test']:
        open_question = element['test']['q']
        print(open_question)
        messages = [
            {"role": "system","content": create_give_answers_to_question()},
            {"role": "user","content": "Potrzebuję odpowiedzi na następujace pytanie: " + open_question}
        ]
        open_answer = create_chat_request(messages,20)
        print(open_answer)
        element['test']['a'] = open_answer

    question = element['question']
    answer = element['answer']
    calculated_answer = eval(question)

    if not calculated_answer == answer:
        print(element['answer'])
        element['answer'] = calculated_answer
        print(element['answer'])

data_json['apikey'] = get_poligon_key()
payload = {
    "task": "JSON",
    "apikey": get_poligon_key(),
    "answer": data_json
}
# print(data_json)
print(requests.post(get_centrala_url() + "/report", json=payload).text)