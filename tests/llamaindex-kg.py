import os
from dotenv import load_dotenv
import logging
import sys
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from IPython.display import Markdown, display
from llama_index.core import StorageContext
from pyvis.network import Network

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

load_dotenv()
OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))

llm = OpenAI(temperature=0, model="gpt-3.5-turbo")  # idk but this expects a temperature < 2
Settings.llm = llm
Settings.chunk_size = 512

documents = SimpleDirectoryReader(
    "../data/processed_files/"
).load_data()

graph_store = SimpleGraphStore()
storage_context = StorageContext.from_defaults(graph_store=graph_store)

index = KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=2,
    storage_context=storage_context,
)

# query using top 3 triplets plus keywords (duplicate triplets are removed)
query_engine = index.as_query_engine(
    include_text=True,
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=5,
)
response = query_engine.query(
    "Make a summary of the story",
)

display(Markdown(f"{response}"))


g = index.get_networkx_graph()
net = Network(notebook=True, cdn_resources="in_line", directed=True)
net.from_nx(g)
net.show("example.html")
