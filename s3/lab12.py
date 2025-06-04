import requests
from qdrant_client import QdrantClient

from utils.utils import create_embedding, create_payload, get_poligon_key, get_centrala_url

question = "W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"

client = QdrantClient(host="localhost", port=6333)
collection = "weapons_reports"

embedding = create_embedding(question)

result = client.search(
    collection_name=collection,
    query_vector=embedding,
    limit=1
)

top_hit = result[0]
print(top_hit.payload["date"])

payload = create_payload("wektory", get_poligon_key(), top_hit.payload["date"])

centrala_answer = requests.post(get_centrala_url() + '/verify', json=payload)
print(centrala_answer.text)