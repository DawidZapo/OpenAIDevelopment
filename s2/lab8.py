import requests

from prompts import create_image_upon_description_prompt
from utils import get_centrala_url, get_poligon_key, create_generate_image_request, create_payload

robot_description = requests.get(get_centrala_url()+ "/data/" + get_poligon_key() + "/robotid.json").text

response = create_generate_image_request(create_image_upon_description_prompt(robot_description))

payload = create_payload("robotid", get_poligon_key(), response)

answer = requests.post(get_centrala_url() + "/verify", json=payload)

print(answer.text)