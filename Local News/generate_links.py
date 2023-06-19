'''
This module invokes other modules and uses Vanguard Catalog List to scrape throught catalogs
to collect all article links
'''

# To invoke other modules
import os
from pathlib import Path

# For logging
import logging

# Create folder if it does not exist already
Path('data_collection\Local News\Vanguard\Logs\\').mkdir(parents=True, exist_ok=True)

# Create and configure logger
LOG_FORMAT = r'%(levelname)s %(asctime)s - %(message)s'
LOGS_FILE_NAME = r'data_collection\Local News\Vanguard\Logs\generate_links.txt'
logging.basicConfig(filename = LOGS_FILE_NAME, level = logging.DEBUG, format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()
logger.info('Generate Links script Launched')

# Global Variable
BASE_STATEMENT = r'python "data_collection\Local News\Vanguard\scrape_catalog.py" --url='

# Scrape links off website
with open(r'data_collection\Local News\Vanguard\Vanguard Catalogs.txt', 'r') as source_file:
    logger.info('Reading lines from Vanguard Catalogs.txt')
    urls = source_file.readlines()
    for url in urls:
        logger.info('Processing URL: %s', url)
        #print('Processing URL: ', url)
        statement = BASE_STATEMENT + url
        try:
            os.system(statement)
            # logger.info('URL processed successfully')
        except Exception as error_description:
            logger.exception(error_description)
