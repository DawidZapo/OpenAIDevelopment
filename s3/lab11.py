import json

import requests

from prompts import create_give_key_words_based_on_reports_and_facts
from utils import read_file_content, create_chat_request, create_payload, get_poligon_key, get_centrala_url

facts_file_paths = [f"../text_files/f0{i}.txt" for i in range(1,10)]
facts = {}
for file_path in facts_file_paths:
    content = read_file_content(file_path)
    facts[file_path.split("/")[-1]] = content

reports_file_paths = [
    '../text_files/2024-11-12_report-00-sektor_C4.txt', '../text_files/2024-11-12_report-01-sektor_A1.txt', '../text_files/2024-11-12_report-02-sektor_A3.txt',
    '../text_files/2024-11-12_report-03-sektor_A3.txt', '../text_files/2024-11-12_report-04-sektor_B2.txt', '../text_files/2024-11-12_report-05-sektor_C1.txt',
    '../text_files/2024-11-12_report-06-sektor_C2.txt', '../text_files/2024-11-12_report-07-sektor_C4.txt', '../text_files/2024-11-12_report-08-sektor_A1.txt',
    '../text_files/2024-11-12_report-09-sektor_C2.txt'
]
reports = {}

for reports_file_path in reports_file_paths:
    content = read_file_content(reports_file_path)
    reports[reports_file_path.split("/")[-1]] = content

messages = [
    {"role": "system", "content": create_give_key_words_based_on_reports_and_facts(reports, facts)},
    {"role": "user", "content": "Podaj odpowiedź"}
]

chat_answer = create_chat_request(messages, 4000, "gpt-4o")

print(chat_answer)

payload = create_payload('dokumenty', get_poligon_key(), json.loads(chat_answer))

centrala_answer = requests.post(get_centrala_url() + '/verify', json=payload)

print(centrala_answer.text)