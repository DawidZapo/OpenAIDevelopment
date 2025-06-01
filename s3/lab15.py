import json

import requests

from neo4j_util.neo4j_util import driver, find_shortest_path, load_users, load_connections
from utils import get_centrala_url, get_poligon_key, read_file_content, get_neo4j_user, get_neo4j_password, \
    create_payload

users_array = json.loads(read_file_content("../text_files/database/users.txt"))['reply']
connections_array = json.loads(read_file_content("../text_files/database/connections.txt"))['reply']

# load_users(users_array)
# load_connections(connections_array)

usernames_array = find_shortest_path("Rafał", "Barbara")
usernames_string = ", ".join(usernames_array)
print(usernames_string)

payload = create_payload("connections", get_poligon_key(), usernames_string)
centrala_answer = requests.post(get_centrala_url() + '/verify', json=payload)
print(centrala_answer.text)



