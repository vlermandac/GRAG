from .preprocess import Preprocess
from .indexing import Indexer


def run(file_path, Client, chunk_size, overlap, embedding_model, dims):
    pp = Preprocess(file_path)
    pages_text, document = pp.read_pdf()
    text_chunks = pp.chunk_text(pages_text, chunk_size, overlap)

    idx = Indexer(Client)
    idx.index_document(document)
    idx.index_text_chunks(text_chunks, document['name'],
                          True, embedding_model, dims)
