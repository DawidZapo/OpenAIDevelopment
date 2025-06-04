from neo4j import GraphDatabase

from utils.utils import get_neo4j_user, get_neo4j_password, get_neo4j_host

driver = GraphDatabase.driver(get_neo4j_host(), auth=(get_neo4j_user(), get_neo4j_password()))

def load_users(users):
    with get_neo4j_driver().session() as session:
        for user in users:
            session.run(
                """
                CREATE (u:User {userId: $userId, username: $username})
                """,
                userId=user["id"],
                username=user["username"]
            )


def load_connections(connections):
    with get_neo4j_driver().session() as session:
        for conn in connections:
            session.run(
                """
                MATCH (u1:User {userId: $userId1})
                MATCH (u2:User {userId: $userId2})
                MERGE (u1)-[:KNOWS]->(u2)
                """,
                userId1=conn["user1_id"],
                userId2=conn["user2_id"]
            )


def find_shortest_path(start_name, end_name):
    query = """
        MATCH (start:User {username: "Rafał"}), (end:User {username: "Barbara"})
        MATCH path = shortestPath((start)-[:KNOWS*]-(end))
        RETURN path
    """
    with driver.session() as session:
        result = session.execute_read(
            lambda tx: tx.run(query, start_name=start_name, end_name=end_name).single()
        )

        if result:
            path = result["path"]
            usernames = [node["username"] for node in path.nodes]
            return usernames
        else:
            return None


def get_neo4j_driver():
    return driver
