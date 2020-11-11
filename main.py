import argparse

import requests
import logging
from pathlib import Path

import hallenbad_data

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s\t%(name)s : %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder")
    return parser.parse_args()


def main():
    logger = logging.getLogger(__name__)

    args = parse_arguments()

    URL = "https://www.stadt-zuerich.ch/ssd/de/index/sport/schwimmen/wassertemperaturen.html"
    output_folder = Path(args.output_folder)

    try:
        logger.info(f"GET url: {URL}")
        page = requests.get(URL)
    except requests.exceptions.RequestException as e:
        logger.error(f"Loading page failed with error: {e}")
        return

    data = hallenbad_data.extract_hallenbad_data(page.content)
    logger.info(f"Extracted hallenbad data: {data}")
    hallenbad_data.store_hallenbad_data(data, output_folder)

    logger.info("Finished downloading data")

if __name__ == '__main__':
    main()
