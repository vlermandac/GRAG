import unittest
import sys
import os
from dotenv import load_dotenv

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, '../src'))

import config  # noqa: E402
import clients  # noqa: E402
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

    def test_openai_client(self):
        client = self.test_clients.open_ai()
        self.assertIsNotNone(client)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Your are the happiest assistant in the world!"},
                {"role": "user",
                 "content": "Hello!"}
            ]
        )
        print(response.choices[0].message)
        self.assertIsNotNone(response.choices[0].message)

    def test_elastic_search_client(self):
        client = self.test_clients.elastic_search()

        client.index(index='test-index', id='1', document={'test': 'test'})
        response = client.get(index='test-index', id='1')
        print(response)
        self.assertIsNotNone(response)
        client.indices.delete(index='test-index')


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
