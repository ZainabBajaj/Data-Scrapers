'''
This script scrapes the passed vanguard catalog link and saves all scaraped
links in a text file by its name in the links folder
'''

# Libraries
from argparse import ArgumentParser # to pass URLs to this script
import re # to find the month
import logging
from subprocess import TimeoutExpired # for logging
#from selenium.webdriver.common.by import By # allows to search by using specific parameters
#from selenium.webdriver.support.ui import WebDriverWait # allows to wait for a PAGE to load
#from selenium.webdriver.support import expected_conditions as EC # determine that webpage has loaded
import undetected_chromedriver.v2 as uc # undetected driver
from pathlib import Path
from time import sleep
from pywinauto import Desktop

# Create and configure logger
LOG_FORMAT = r'%(levelname)s %(asctime)s - %(message)s'
LOGS_FILE_NAME = r'data_collection\Local News\Vanguard\Logs\scrape_vanguard.txt'
logging.basicConfig(filename = LOGS_FILE_NAME, level = logging.INFO, format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()
logger.info('Scrape Catalog script Launched')

# argument parsing
parser = ArgumentParser()
parser.add_argument('--url', type = str, required = True,
                    help = 'write URL of PAGE 1 of the catalog')

# Constants
URL = parser.parse_args().url
#URL = 'https://www.vanguardngr.com/2019/1/' # for testing
logger.info('--URL argument received: %s', URL)
year = URL[28:32]
month = (re.findall('[0-9]+', URL[32:]))[0]
logger.info('URL refers to year %s and month %s', year, month)
pages = [1]
PAGE = pages[0]
LAST_PAGE = 999
WAIT = 15
SLEEP = 30
RECOVERY_PROCESS_FLAG = False

# create an instance of chrome
browser = uc.Chrome()
browser.implicitly_wait(WAIT)
logger.info('Chrome instance created')

# Create folder if it does not exist already
Path('data_collection\Local News\Vanguard\Links\\').mkdir(parents=True, exist_ok=True)

# open the file
LINKS_FILE_TITLE = r'data_collection\Local News\Vanguard\Links\links_' + str(year) + '_' + str(month) + '.txt'
with open (LINKS_FILE_TITLE, 'w') as links_file:
    logger.info('Starting scraping')
    while PAGE < LAST_PAGE:

        if PAGE == 1 or RECOVERY_PROCESS_FLAG == True:
            browser.get(URL)
            if PAGE == 1: print('Initiated Activity. Scrapping:\nPage: base page')
            logger.info('PAGE 1/Process Recovery subroutine executed successfully')
            RECOVERY_PROCESS_FLAG = False
        if LAST_PAGE == 999:
            # find buttons and update pages list
            buttons = browser.find_elements_by_xpath('//*[@id="main"]/div/div/nav/div/a')
            for button in buttons:
                try:
                    pages.append(int(button.text))
                except:
                    pass
            LAST_PAGE = pages[-1]
            logger.info('Last PAGE identifed as: %s', LAST_PAGE)

        # scrape all links without duplicates
        print('PAGE: ', PAGE)
        logger.info('Scraping page : %s', PAGE)
        URLs = []
        logger.info('Looping through the elements returned by xPath')
        for element in browser.find_elements_by_xpath("//a[@href]"):
            LINK = str(element.get_attribute('href'))
            if year not in LINK or 'PAGE' in LINK:
                continue
            if LINK in URLs:
                #print('duplicate URL, continuing to next LINK')
                continue
            URLs.append(LINK)
            links_file.write(LINK)
            links_file.write('\n')
        logger.info('Unique links written to text file')
        
        try:
            # click next
            buttons = browser.find_elements_by_class_name('page-numbers')
            button = buttons[-1].click()
            logger.info('Next button clicked')
            # WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located(
            #     (By.XPATH, '//*[@id="masthead"]/div[1]/div[1]/div[1]/a/img')))
            #URL = browser.current_URL
            #chrome_window = Desktop(backend="uia").window(class_name_re='Chrome')
            #address_bar_wrapper = chrome_window['Google Chrome'].main.Edit.wrapper_object()
            #url_1 = address_bar_wrapper[0].legacy_properties()['Value']
            #url_2 = address_bar_wrapper.iface_value.CurrentValue
            #print(url_1)
            #print(url_2)
            #PAGE = int(re.search('[0-9]+', URL[34:]).group(0))
        # except TimeoutExpired:
        #     print('URL timed out. Timeout window: ', TIMEOUT)
        #     browser.quit()
        #     print('Running the URL again')
            sleep(2)
            PAGE += 1

        except Exception as some_other_exception:
            print('AN EXCEPTION OCCURED! Sleeping for', SLEEP, 'seconds')
            browser.quit()
            print(some_other_exception)
            sleep(SLEEP)
            print('Restoring browser to last URL')
            browser = uc.Chrome()
            RECOVERY_PROCESS_FLAG = True
            logger.exception(some_other_exception)
            #print('Exception Logged')
            #continue
            