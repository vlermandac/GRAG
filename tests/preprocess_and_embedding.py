import unittest
import sys
import os
from dotenv import load_dotenv

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, '../src'))

import config  # noqa: E402
import clients  # noqa: E402
from data_loading import indexing, preprocess  # noqa: E402
from pretty_test_runner import RichTestRunner  # noqa: E402


class TestElasticsearch(unittest.TestCase):
    def setUp(self):
        config.setup_variables('../')
        load_dotenv()
        ELASTIC_PASSWORD = str(os.getenv("ELASTIC_PASSWORD"))
        ELASTIC_URL = str(os.getenv("ELASTIC_URL"))
        CA_CERT = '../' + str(os.getenv("CA_CERT"))
        OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))

        self.test_clients = clients.Client(
                ELASTIC_URL, ELASTIC_PASSWORD, CA_CERT, OPENAI_API_KEY)

        self.pp = preprocess.Preprocess("files/Noctulo-Ricardo_Meruane.pdf")
        self.idx = indexing.Indexer(self.test_clients)

    def test_preprocess(self):
        pages, info = self.pp.read_pdf()
        self.assertIsNotNone(info['text'])

        #  with open("files/expected.txt", 'r') as f:
        #   expected_text = f.read()
        #   self.assertEqual(info['text'], expected_text)

        self.chunks = self.pp.chunk_text(pages, chunk_size=10, overlap_size=1)

        self.idx.index_document(info)

        doc_name = info['name']

        response = \
            self.test_clients.elastic_search().get(
                    index='document', id=doc_name)
        self.assertIsNotNone(response)

        self.test_clients.elastic_search().delete(
                index='document', id=doc_name)

        print(self.chunks)

        self.idx.index_text_chunks(self.chunks, doc_name, True,
                                   'text-embedding-3-small', 10)

        response = self.test_clients.elastic_search().search(
                index=f'{doc_name}-chunk',
                body={"query": {"match_all": {}}})
        self.assertIsNotNone(response)

        self.test_clients.elastic_search().indices.delete(
                index=f'{doc_name}-chunk')


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
