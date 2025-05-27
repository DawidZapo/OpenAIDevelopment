from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from utils import read_file_content, create_embedding

quadrant_client = QdrantClient(host="localhost", port=6333)

collection_name = 'weapons_reports'
dimension = 3072

quadrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
)

def extract_date_from_filename(filename: str):
    return filename.split("/")[-1].replace("_", "-").replace(".txt", "")

file_paths = [
    '../text_files/secret/2024_01_08.txt', '../text_files/secret/2024_01_17.txt', '../text_files/secret/2024_01_27.txt', '../text_files/secret/2024_01_29.txt','../text_files/secret/2024_02_01.txt',
    '../text_files/secret/2024_02_11.txt','../text_files/secret/2024_02_15.txt','../text_files/secret/2024_02_21.txt','../text_files/secret/2024_03_02.txt','../text_files/secret/2024_03_12.txt',
    '../text_files/secret/2024_03_15.txt','../text_files/secret/2024_03_18.txt','../text_files/secret/2024_03_19.txt','../text_files/secret/2024_03_25.txt','../text_files/secret/2024_03_29.txt',
    '../text_files/secret/2024_03_31.txt','../text_files/secret/2024_04_18.txt','../text_files/secret/2024_04_27.txt','../text_files/secret/2024_05_08.txt','../text_files/secret/2024_05_14.txt',
    '../text_files/secret/2024_05_31.txt','../text_files/secret/2024_06_02.txt','../text_files/secret/2024_07_05.txt'
]

points = []

for idx, path in enumerate(file_paths):
    content = read_file_content(path)
    embedding = create_embedding(content)
    date = extract_date_from_filename(path)

    point = PointStruct(
        id=idx,
        vector=embedding,
        payload={"date": date, "filename": path}
    )

    points.append(point)

quadrant_client.upsert(collection_name=collection_name, points=points)