class Indexer:
    def __init__(self, Client):
        self.es_client = Client.elastic_search()
        self.oa_client = Client.open_ai()

    def index_document(self, document):
        self.es_client.index(index='document',
                             id=document['name'],
                             body={'name': document['name'],
                                   'author': document['author'],
                                   'text': document['text']})

    def index_text_chunks(self, chunks, document_name, index_embeddings,
                          embedding_model, dims):
        chunks_mapping = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "init_page": {"type": "integer"},
                    "embedding": {"type": "dense_vector", "dims": dims}
                }
            }
        }

        index_name = f"{document_name}-chunk"
        self.es_client.indices.create(index=index_name,
                                      body=chunks_mapping, ignore=400)

        for i, chunk in enumerate(chunks):
            properties = {
                'text': chunk[0],
                'init_page': chunk[1][0]
            }
            if index_embeddings:
                properties['embedding'] = \
                    self.generate_embedding(chunk[0], embedding_model, dims)

            self.es_client.index(index=index_name, id=i, body=properties)

    def generate_embedding(self, text, embedding_model, dims):
        response = self.oa_client.embeddings.create(
            input=[text],
            model=embedding_model,
            dimensions=dims
        )
        return response.data[0].embedding
