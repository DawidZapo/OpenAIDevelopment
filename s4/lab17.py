import requests
from utils.utils import openai_client, create_chat_request, create_payload, get_poligon_key, get_centrala_url

data = {}

with open("../text_files/fine_tune/verify.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)
            data[key] = value

messages = [
    {"role": "user", "content": ""}
]

for key, value in data.items():

    messages[0]['content'] = value

    answer = create_chat_request(messages,300, "ft:gpt-4o-mini-2024-07-18:personal:mine-fine-tune:BecuYAUn")
    print(answer)
    data[key] = answer

answers = []
for key, value in data.items():
    if value == '1':
        answers.append(key)

payload = create_payload("research", get_poligon_key(), answers)
centrala_answer = requests.post(get_centrala_url() + '/verify', json=payload)
print(centrala_answer.text)