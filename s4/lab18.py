import json
import time

from markdownify import markdownify as md
import requests
from bs4 import BeautifulSoup

from prompts import create_ask_if_answer_is_possible_prompt, create_answer_question_based_on_html, \
    create_ask_which_link_prompt
from s3.lab11 import reports
from utils.utils import get_centrala_url, get_poligon_key, openai_client, get_softo_url, create_payload, \
    create_chat_request


def get_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = md(str(soup))
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    return text, links


def ask_if_answer_possible(page_text, question):
    messages=[{"role": "user", "content": create_ask_if_answer_is_possible_prompt(page_text, question)}]
    response = create_chat_request(messages, 100)
    return "tak" in response.lower()


def ask_for_answer(page_text, question):
    messages=[{"role": "user", "content": create_answer_question_based_on_html(question, page_text)}]
    response = create_chat_request(messages, 300)
    return response.strip()

def ask_which_link(page_text, question, links):
    messages=[{"role": "user", "content": create_ask_which_link_prompt(page_text, question, links)}]
    response = create_chat_request(messages, 300)
    return response.strip()

def crawl_for_question(question_text):
    visited = set()
    to_visit = [get_softo_url()]

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            page_text, links = get_page(current_url)
        except Exception as e:
            print(f" Error: {e}")
            continue

        if ask_if_answer_possible(page_text, question_text):
            return ask_for_answer(page_text, question_text)

        next_link = ask_which_link(page_text, question_text, links)
        if next_link.startswith("/"):
            next_link = get_softo_url() + next_link
        if next_link not in visited:
            to_visit.append(next_link)

        time.sleep(1)

    return "Nie znaleziono odpowiedzi."

questions = json.loads(requests.post(get_centrala_url() + '/data/' + get_poligon_key() + '/softo.json').text)
print(questions)

answers = {}

for qid, question in questions.items():
    answer = crawl_for_question(question)
    answers[qid] = answer

print(answers)

payload = create_payload("softo", get_poligon_key(), answers)
centrala_answer = requests.post(get_centrala_url() + '/verify', json=payload)

print(centrala_answer.text)