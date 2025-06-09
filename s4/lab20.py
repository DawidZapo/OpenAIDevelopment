import json
import fitz
import requests
from pdf2image import convert_from_path

from prompts import create_answer_questions_based_on_pdf
from utils.utils import get_centrala_url, get_poligon_key, create_chat_request, \
    create_process_image_request, create_payload

questions = json.loads(requests.post(get_centrala_url() + '/data/' + get_poligon_key() + '/notes.json').text)
print(questions)

def extract_text_pages(path="../pdf_files/notatnik-rafala.pdf", start=0, end=17):
    doc = fitz.open(path)
    text = ""
    for page_num in range(start, end + 1):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_page19(path="../pdf_files/notatnik-rafala.pdf"):
    images = convert_from_path(path, first_page=19, last_page=19)
    image = images[0]
    image.save('../pdf_files/page19.png', 'PNG')
    return create_process_image_request(['../pdf_files/page19.png'], 'Na podstawie obrazu, spróbuj wyodrębnić zawarty w nim tekst. Wiem, że grafika może nie być najbardziej wyraźna ale postaraj się wyłapać jakiekolwiek zdania z niej.')

def ask_question(context, question, previous_answer=None, hint=None):
    messages = [
        {"role": "system", "content": create_answer_questions_based_on_pdf(context)},
        {"role": "user", "content": "Odpowiedz na pytania"}
    ]

    if previous_answer and hint:
        messages.append({
            "role": "user",
            "content": f"Twoja poprzednia odpowiedź brzmiała: {previous_answer} i była błędna.\nPodpowiedź: {hint}.\nNie używaj błędnej odpowiedzi.\nSpróbuj ponownie."
        })

    messages.append({"role": "user", "content": f"Pytanie: {question}"})

    return create_chat_request(messages, 200)


text_1_to_18 = extract_text_pages()
text_19 = extract_text_from_page19()
full_context = text_1_to_18 + ". " + text_19

answers = {}
for qid, question in questions.items():
    answer = ask_question(full_context, question)
    answers[qid] = answer

print(answers)

payload = create_payload("notes", get_poligon_key(), answers)

centrala_answer = json.loads(requests.post(get_centrala_url() + '/verify', json=payload).text)
print(centrala_answer)

