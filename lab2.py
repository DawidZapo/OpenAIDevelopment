import json
import re
import requests
from chat_request import get_xyz_url, create_chat_request
from prompts import create_give_answers_to_question_based_on_context_prompt

html_content = requests.get(get_xyz_url() + "/files/0_13_4b.txt").text

# print(html_content)
payload = {
    "text":"READY",
    "msgID":"0"
}

match = re.search(r"takie jak:(.*?)(Pamiętaj, że)", html_content, re.DOTALL)

misleading_info = ''
if match:
    misleading_info = match.group(1).strip()


response1 = json.loads(requests.post(get_xyz_url() + "/verify", json=payload).text)
msgID = response1["msgID"]
question = response1["text"]
print(question)

messages = [
    {
        "role": "system",
        "content": create_give_answers_to_question_based_on_context_prompt(misleading_info)
    },
    {
        "role": "user",
        "content": "Potrzebuję odpowiedzi na następujace pytanie: " + question
    }
]
chat_answer = create_chat_request(messages, 10)
print(chat_answer)


payload["msgID"] = msgID
payload["text"] = chat_answer
response2 = requests.post(get_xyz_url() + "/verify", json=payload)
print(response2.text)