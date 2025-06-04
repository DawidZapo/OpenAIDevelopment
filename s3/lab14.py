import json

import requests

from prompts import create_extract_people_and_cities_prompt
from utils.utils import get_centrala_url, create_chat_request, get_poligon_key

notes = requests.get(get_centrala_url() + '/dane/barbara.txt').text

print(notes)

messages = [
    {"role": "system", "content": create_extract_people_and_cities_prompt(notes)},
    {"role": "user", "content": "Podaj listę ludzi oraz miast. Pamiętaj bez polskich znaków"}
]

people_and_cities = json.loads(create_chat_request(messages, 300))

def get_people_from_place(city: str):
    response = requests.post(get_centrala_url() + '/places', json={"apikey": get_poligon_key(), "query": city}).text
    return json.loads(response)['message']

def get_cities_from_person(person: str):
    response = requests.post(get_centrala_url() + '/people', json={"apikey": get_poligon_key(), "query": person}).text
    return json.loads(response)['message']

visited_people = set()
visited_cities = set()

people_queue = []
cities_queue = []

starting_people = people_and_cities['people']

for person in starting_people:
    people_queue.append(person)
    visited_people.add(person)


while people_queue or cities_queue:
    while people_queue:
        person = people_queue.pop(0)
        city_data = get_cities_from_person(person)

        if "[**RESTRICTED DATA**]" in city_data:
            continue

        for city in city_data.split():
            city = city.strip()
            if city and city not in visited_cities:
                visited_cities.add(city)
                cities_queue.append(city)


    while cities_queue:
        city = cities_queue.pop(0)
        people_data = get_people_from_place(city)

        if "[**RESTRICTED DATA**]" in people_data:
            continue

        for person in people_data.split():
            person = person.strip()
            person_upper = person.upper()
            if person_upper == "BARBARA":
                print(f"Znaleziono Barbarę w mieście: {city}")
                exit(0)

            if person and person not in visited_people:
                visited_people.add(person)
                people_queue.append(person)