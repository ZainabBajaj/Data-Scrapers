'''
This code generates a txt file titled 'Vanguard Catalogs'
that contains links for catalogs from January 2019 to May 2021
'''

# external tools
from datetime import datetime

# constants
YEAR_RANGE_BEGIN = 2019
YEAR_RANGE_END = 2021
FIXED_URL_COMPONENT = 'https://www.vanguardngr.com/'
LINKS = []

# populate list LINKS
for year in range (YEAR_RANGE_BEGIN, YEAR_RANGE_END + 1):
    for month in range (1,13):
        # generate url
        URL = FIXED_URL_COMPONENT + str(year) + '/' + str(month) + '/'
        # print url for diagnosis
        print(URL)
        # append url
        LINKS.append(URL)

# remove links that will not work
today = datetime.today()
LATEST_LINK = FIXED_URL_COMPONENT + str(today.year) + '/' + str(today.month) + '/'
LINKS = LINKS[:LINKS.index(LATEST_LINK) + 1]

with open ('data_collection\Local News\Vanguard\Vanguard Catalogs.txt', 'w') as links_file:
    for link in LINKS:
        links_file.write(link)
        links_file.write('\n')

print('Run complete')
