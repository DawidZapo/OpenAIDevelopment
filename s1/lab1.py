from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from utils import get_xyz_url, create_chat_request, get_username, get_pass

html_content = requests.get(get_xyz_url()).text
soup = BeautifulSoup(html_content, "html.parser")
question_element = soup.find(id="human-question")
question = question_element.get_text(separator=" ", strip=True).replace("Question:", "").strip()
print(question)

messages = [
    {"role": "user", "content": "Potrzebuję odpowiedzi na następujące pytanie, podaj tylko rok: " + question}
]

answer = create_chat_request(messages, 3)
print(answer)

payload = {
    "username": get_username(),
    "password": get_pass(),
    "answer": answer
}

response = requests.post(get_xyz_url(), data=payload)

# print("Status code:", response.status_code)
# print("Response text:", response.text)

