import json

import requests

from prompts import create_give_sql_query_prompt
from utils import get_centrala_url, create_payload, get_poligon_key, create_query_payload, create_chat_request

connections_metadata = json.loads(requests.post(get_centrala_url() + '/apidb', json=create_query_payload("database", get_poligon_key(), "show create table connections")).text)
correct_order_metadata = json.loads(requests.post(get_centrala_url() + '/apidb', json=create_query_payload("database", get_poligon_key(), "show create table correct_order")).text)
datacenters_metadata = json.loads(requests.post(get_centrala_url() + '/apidb', json=create_query_payload("database", get_poligon_key(), "show create table datacenters")).text)
users_metadata = json.loads(requests.post(get_centrala_url() + '/apidb', json=create_query_payload("database", get_poligon_key(), "show create table users")).text)

messages = [
    {"role": "system", "content": create_give_sql_query_prompt([connections_metadata, correct_order_metadata, datacenters_metadata, users_metadata])},
    {"role": "user", "content": "Podaj zapytanie SQL"}
]

chat_given_sql = create_chat_request(messages, 300)

database_answer = json.loads(requests.post(get_centrala_url() + '/apidb', json=create_query_payload("database", get_poligon_key(), chat_given_sql)).text)

id_array = [item['dc_id'] for item in database_answer['reply']]

centrala_answer = requests.post(get_centrala_url() + '/verify', json=create_payload('database', get_poligon_key(), id_array))

print(centrala_answer.text)
