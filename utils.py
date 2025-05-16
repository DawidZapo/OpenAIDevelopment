import os

from dotenv import load_dotenv
from langfuse import Langfuse
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_host = os.getenv("LANGFUSE_HOST")
poligon_key = os.getenv("POLIGON_KEY")
xyz_url = os.getenv("XYZ_URL")
centrala_url = os.getenv("CENTRALA_URL")
password = os.getenv("PASSWORD")
username = os.getenv("USERNAME")

client = OpenAI(api_key=api_key)
langfuse_client = Langfuse(
    secret_key=langfuse_secret_key,
    public_key=langfuse_public_key,
    host=langfuse_host
)

def create_chat_request(messages: [], tokens: int):

    trace = langfuse_client.trace(name="chat-request", user_id="dawidzapo")
    span = trace.span(name="openai.chat.completion", input=messages)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=tokens
        )

        span.end(output=response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        span.end(error_message=str(e))
        raise

def get_xyz_url():
    return xyz_url

def get_centrala_url():
    return centrala_url

def get_poligon_key():
    return poligon_key

def get_username():
    return username

def get_pass():
    return password

def create_payload(task: str, apikey: str, answer):
    return {
        "task": task,
        "apikey": apikey,
        "answer": answer
    }