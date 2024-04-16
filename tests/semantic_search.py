import sys
import os
from dotenv import load_dotenv

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, '../src'))

import clients  # noqa: E402

load_dotenv()

ELASTIC_PASSWORD = str(os.getenv("ELASTIC_PASSWORD"))
ELASTIC_URL = str(os.getenv("ELASTIC_URL"))
CA_CERT = '../' + str(os.getenv("CA_CERT"))
OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))

test_clients = clients.Client(
        ELASTIC_URL, ELASTIC_PASSWORD, CA_CERT, OPENAI_API_KEY)

client = test_clients.elastic_search()
client2 = test_clients.open_ai()

vector_query = client2.embeddings.create(
    input="Make a summary of the script",
    model="text-embedding-3-small",
    dimensions=200
).data[0].embedding


def pretty_response(response):
    if len(response["hits"]["hits"]) == 0:
        print("Your search returned no results.")
    else:
        for hit in response["hits"]["hits"]:
            id = hit["_id"]
            score = hit["_score"]
            text = hit["_source"]["text"]
            pretty_output = f"""
                            \nID: {id}\n{score}\n{text}\n
                            """
            print(pretty_output)


response = client.search(
    index="goodfellas-chunk",
    knn={
        "field": "embedding",
        "query_vector": vector_query,
        "k": 5,
        "num_candidates": 20,
    },
)

pretty_response(response)
