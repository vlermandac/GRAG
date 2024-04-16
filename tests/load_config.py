import unittest
import sys
import os

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, '../src'))

import config  # noqa: E402
from pretty_test_runner import RichTestRunner  # noqa: E402


class TestElasticsearch(unittest.TestCase):
    def setUp(self):
        self.config_variables = config.setup_variables(project_root='../')
        self.expected_config_variables = [
            'env-variables',
            'project_root',
            'openai_api_key',
            'elastic_url',
            'elastic_password',
            'ca_cert',
            'data',
            'unprocessed-files',
            'processed-files',
            'preprocess',
            'chunk-size',
            'overlap',
            'embedding',
            'dimension',
            'openai-model',
            'test_control_variable',
            'do_not_delete'
        ]

    def test_config_variables(self):
        control_variable = self.config_variables.list['test_control_variable']
        self.assertEqual(control_variable['do_not_delete'], None)

        obtained_variables = []
        for section in self.config_variables.list:
            obtained_variables.append(section)
            for values in self.config_variables.list[section]:
                if (type(values) is dict):
                    for key in values.keys():
                        obtained_variables.append(key)
                else:
                    obtained_variables.append(values)

        self.assertListEqual(obtained_variables,
                             self.expected_config_variables,
                             "The config variables are not as expected")


if __name__ == '__main__':
    unittest.main(testRunner=RichTestRunner())
