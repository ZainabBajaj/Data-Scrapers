'''
This module invokes other modules and uses text files from Links folder 
to scrape through articles
'''

# To invoke other modules
import os
from pathlib import Path

# For logging
import logging

# Create folder if it does not exist already
#Path('data_collection\Local News\Vanguard\Links\\').mkdir(parents=True, exist_ok=True)

# Create and configure logger
LOG_FORMAT = r'%(levelname)s %(asctime)s - %(message)s'
LOGS_FILE_NAME = r'data_collection\Local News\Vanguard\Logs\scrape_data.txt'
logging.basicConfig(filename = LOGS_FILE_NAME, level = logging.DEBUG, format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()
logger.info('Scrape Data script Launched')


# Global Variable
BASE_STATEMENT = r'python "data_collection\Local News\Vanguard\scrape_articles.py" --text_file='
LINKS_FOLDER_PATH = r'data_collection\Local News\Vanguard\Links\\'
CATALOGS = os.listdir(LINKS_FOLDER_PATH)
logger.info('Reading lines from Links folder')

for catalog in CATALOGS:
    logger.info('Processing Catalog: %s', catalog)
    statement = BASE_STATEMENT + '"' + LINKS_FOLDER_PATH + catalog + '"'
    try:
        os.system(statement)
        logger.info('Catalog completed.')
    except Exception as error_description:
        logger.exception(error_description)
