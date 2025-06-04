import requests

from utils.utils import get_centrala_url, get_poligon_key, create_chat_request, create_payload
from prompts import create_anonymize_personal_data_prompt

data_to_anonymize = requests.get(get_centrala_url() + "/data/" + get_poligon_key() + "/cenzura.txt").text

print(data_to_anonymize)

messages = [
    {"role" : "system", "content" : create_anonymize_personal_data_prompt()},
    {"role": "user", "content": "Dokonaj anomizacji danych: " + data_to_anonymize}
]
answer = create_chat_request(messages, 100)

print(answer)

payload = create_payload("CENZURA", get_poligon_key(), answer)

response = requests.post(get_centrala_url() + "/report", json=payload)

print(response.text)