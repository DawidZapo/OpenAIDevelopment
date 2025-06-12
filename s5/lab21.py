import base64
import json

import requests

from prompts import create_find_imposter_among_dialogues_prompt, create_recognize_city_prompt, \
    recognize_names_based_on_context, create_answer_questions_based_on_talks_and_facts
from utils.utils import get_centrala_url, get_poligon_key, read_file_content, get_coded_url, create_chat_request

phone_data = json.loads(requests.get(base64.b64decode(get_coded_url()).decode("utf-8").replace("TUTAJ-KLUCZ", get_poligon_key())).text)
phone_questions = json.loads(requests.get(get_centrala_url() + '/data/' + get_poligon_key() + '/phone_questions.json').text)
print(phone_questions)

facts_paths = [f'../text_files/f0{i}.txt' for i in range (1,10)]

facts = []
for fact_path in facts_paths:
    facts.append(read_file_content(fact_path))

print(facts)

phone_data_with_names = json.loads(read_file_content('./phone_data_with_names.json'))
print(phone_data_with_names)

chat_answers = {}
for key, question in phone_questions.items():
    print(question)
    messages = [
        {"role": "system", "content": create_answer_questions_based_on_talks_and_facts(str(phone_data_with_names) + ". a to fakty, które też się przydzadzą: " + str(facts))},
        {"role": "user", "content": question}
    ]
    answer = create_chat_request(messages, 4024, model="gpt-4o")
    print(answer)
    chat_answers[key] = answer





