import os
import sys
import argparse
import re
from dotenv import load_dotenv

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, './src'))

import config  # noqa: E402
import data_loading  # noqa: E402
from clients import Client  # noqa: E402
from utils import logger  # noqa: E402

if (len(sys.argv) != 2) and (len(sys.argv) != 3):
    logger.error("No arguments provided.", "num", str(len(sys.argv)))
    sys.exit(1)

logger.info("Execution started.", "dir", pwd)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--process_data", help="Process files", action="store_true")
group.add_argument("--RAG", help="Run RAG", action="store_true")
group.add_argument("--KG", help="Run KG", action="store_true")
args = parser.parse_args()

logger.info("Arguments parsed.", "flags", str(sys.argv[1:]))


config_variables = config.setup_variables(project_root='./')

logger.info("Config variables parsed and loaded.", "", "")

load_dotenv()
ELASTIC_PASSWORD = str(os.getenv("ELASTIC_PASSWORD"))
ELASTIC_URL = str(os.getenv("ELASTIC_URL"))
CA_CERT = str(os.getenv("CA_CERT"))
OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))

logger.info("Environment variables loaded.", "path", "./.env")

clients = Client(ELASTIC_URL, ELASTIC_PASSWORD, CA_CERT, OPENAI_API_KEY)
logger.info("Clients created and connected.", "", "")

if args.process_data:
    DATA_DIRECTORY = config_variables.list['data']['unprocessed-files']
    logger.info("Reading files...", "dir", DATA_DIRECTORY)

    for file in os.listdir(DATA_DIRECTORY):
        logger.info("Processing file.", "file", file)

        full_path = os.path.join(DATA_DIRECTORY, file)
        if not os.path.isfile(full_path):
            continue
        if not re.match(r'^[^-]+-[^-]+\.pdf$', file):
            print(f"""Error: The file '{file}' does not match
                  the expected format 'author_name-title_name.pdf'.""")
            sys.exit(1)

        data_loading.run(full_path, clients,
                         config_variables.list['preprocess']['chunk-size'],
                         config_variables.list['preprocess']['overlap'],
                         config_variables.list['embedding']['openai-model'],
                         config_variables.list['embedding']['dimension'])
        logger.info("Data loaded and processed.", "", "")

    os.system(f"""mv {DATA_DIRECTORY}/*.pdf
              {config_variables.list['data']['processed-files']}""")

    logger.info("Processed files moved.", "dir",
                config_variables.list['data']['processed-files'])

if args.RAG:
    # Implementation for RAG
    print("RAG processing not implemented.")
    pass

if args.KG:
    # Implementation for KG
    print("KG processing not implemented.")
    pass
