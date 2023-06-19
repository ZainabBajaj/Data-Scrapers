from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--usagedisable-dev-shm-')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)




def getURL(url):
  yt_links = []
  driver =webdriver.Chrome('chromedriver',chrome_options=chrome_options)
  driver.get(url)

  duration_list = []
  for i in range(10):
      #scroll 1000 px
      driver.execute_script('window.scrollTo(0,(window.pageYOffset+1000))')
      sleep(3)
      elements = driver.find_elements_by_xpath('//*[@id="video-title"]')
      for element in elements:
          yt_links.append(element.get_attribute('href'))

  return yt_links


  urls = ["https://www.youtube.com/results?search_query=gender+based+violence+nigeria", "https://www.youtube.com/results?search_query=domestic+violence+nigeria",
        "https://www.youtube.com/results?search_query=gender+equality+nigeria", "https://www.youtube.com/results?search_query=endgbv+nigeria", "https://www.youtube.com/results?search_query=violence+against+women+nigeria",
        "https://www.youtube.com/results?search_query=mental+health+nigeria"]

for url in urls:
  links = getURL(url)
    
