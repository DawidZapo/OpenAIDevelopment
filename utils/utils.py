import os
import tiktoken
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
neo4j_password = os.getenv("NEO_4J_PASSWORD")
neo4j_user = os.getenv("NEO_4J_USER")
neo4j_host = os.getenv("NEO_4J_HOST")
softo_url = os.getenv("SOFTO_URL")
coded_url = os.getenv("CODED_URL")

openai_client = OpenAI(api_key=api_key)
langfuse_client = Langfuse(
    secret_key=langfuse_secret_key,
    public_key=langfuse_public_key,
    host=langfuse_host
)

def create_chat_request(messages: [], tokens: int, model: str = "gpt-4") :

    trace = langfuse_client.trace(name="chat-request", user_id="dawidzapo")
    span = trace.span(name="openai.chat.completion", input=messages)

    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=tokens
        )

        span.end(output=response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        span.end(error_message=str(e))
        raise

def create_transcribe_request(file_path: str):

    trace = langfuse_client.trace(name="audio-request", user_id="dawidzapo")
    span = trace.span(name="openai.audio.transcription", input={"file_path": file_path, "language": "pl"})

    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pl",
                response_format="text"
            )
        span.end(output=transcript)
        return transcript

    except Exception as e:
        span.end(error_message=str(e))
        raise


def create_process_image_request(image_paths: list[str], prompt: str):
    trace = langfuse_client.trace(name="multi-image-request-gpt4o", user_id="dawidzapo")
    span = trace.span(name="openai.gpt4o.multi-image", input={"image_paths": image_paths, "prompt": prompt})

    try:
        import base64
        content_blocks = [{"type": "text", "text": prompt}]

        for image_path in image_paths:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                mime_type = "image/png"
                base64_image = base64.b64encode(image_data).decode("utf-8")

                content_blocks.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}"
                    }
                })

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": content_blocks
                }
            ],
            max_tokens=1000
        )

        span.end(output=response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        span.end(error_message=str(e))
        raise

def create_process_image_request_from_urls(image_urls: list[str], prompt: str):
    trace = langfuse_client.trace(name="multi-image-url-request-gpt4o", user_id="dawidzapo")
    span = trace.span(name="openai.gpt4o.multi-image-url", input={"image_urls": image_urls, "prompt": prompt})

    try:
        content_blocks = [{"type": "text", "text": prompt}]

        for image_url in image_urls:
            content_blocks.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            })

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": content_blocks
                }
            ],
            max_tokens=1000
        )

        span.end(output=response.choices[0].message.content)
        return response.choices[0].message.content

    except Exception as e:
        span.end(error_message=str(e))
        raise


def create_generate_image_request(prompt: str, size: str = "1024x1024"):
    trace = langfuse_client.trace(name="image-generation-request", user_id="dawidzapo")
    span = trace.span(name="openai.images.generate", input={"prompt": prompt, "size": size})

    try:
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            n=1,
            response_format="url"
        )

        image_url = response.data[0].url
        span.end(output=image_url)
        return image_url

    except Exception as e:
        span.end(error_message=str(e))
        raise

def split_text_by_tokens(text, max_tokens=2000, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

def create_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding

def read_file_content(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        content =  file.read()
        return content



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

def create_query_payload(task: str, apikey: str, query):
    return {
        "task": task,
        "apikey": apikey,
        "query": query
    }

def get_neo4j_password():
    return neo4j_password

def get_neo4j_user():
    return neo4j_user

def get_neo4j_host():
    return neo4j_host

def get_softo_url():
    return softo_url

def get_coded_url():
    return coded_url