'''
This script reads links from monthly catalog text files, 
remove duplicates and opens each article to scrape article items
into a csv. 

'''

# External resources
from argparse import ArgumentParser
import pandas as pd
import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path

# argument parsing
parser = ArgumentParser()
parser.add_argument('--text_file', type = str, required = True,
                    help = 'write file path of the text file containing the links')

# constants
text_file = parser.parse_args().text_file
#text_file = r'data_collection\Local News\Vanguard\Links\links_2019_1.txt' # for testing
column_names = ['URL', 'Title', 'Content', 'Published/Updated']
TIMEOUT = 30 # 30s timeout

# Remove duplicates and create dataframe
df_raw = pd.read_csv(text_file, names = column_names)
df = df_raw.drop_duplicates()

duplicate_count = df_raw.shape[0] - df.shape[0]

other_removals = df.shape[0]
df = df[~df.URL.str.contains('#content')]
df = df[~df.URL.str.contains('/page/')]
other_removals = other_removals - df.shape[0]

print('Duplicates removed:', duplicate_count, '\nOther removals:', other_removals, '\nArticles in the link:', df.shape[0])

# scrape 
iteration = 0

for url in df['URL']:
    iteration += 1
    
    print('Article: ', iteration)
    
    # create an instance of Chrome
    if iteration == 1: browser = uc.Chrome()
    
    try:
        # load url
        browser.get(url)
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="masthead"]/div[1]/div[1]/div[1]/a/img')))
        
        # get elements
        try:
            title = browser.find_element_by_css_selector('h1.entry-title').text
        except:
            title = ''    
        try:
            main_content = browser.find_element_by_css_selector('div.main-content').text
        except:
            main_content = ''
        try:
            date = browser.find_element_by_css_selector('time.entry-date').text
        except:
            date =''

        # append to csv
        df.iloc[iteration - 1, 1] = title
        df.iloc[iteration - 1, 2] = main_content
        df.iloc[iteration - 1, 3] = date

        #if iteration == 5:
        #    break

    except TimeoutException:
        print('Timed out while waiting for page to load')


browser.close()

# write csv to storage
text_tokens = text_file.split('_')
Path('data_collection\Local News\Vanguard\Data\\').mkdir(parents=True, exist_ok=True)
CSV_TITLE = r'data_collection\\Local News\\Vanguard\Data\\' + text_tokens[-2] + '_' + text_tokens[-1].split('.')[0] + '.csv'
df.to_csv(CSV_TITLE)
