# LinkedIn Scrapping

This scrapping was carried out on linkedin posts using a list of just over 100 GBV keywords. The posts scraped were filtered based on location of profile owner being Nigeria.

### Method of Data Collection:
1.	Links to 'All Posts' were generated using the aforementioned keywords.
2.	Phantom buster's post scraper and linkedin profile scraper were used to scrape posts from the above generated links and scrape the profile details of the profiles of the scraped posts respectively.
3.	Results from both scrapes were merged and filtered based on location on profile owner being Nigeria. 

### Problem's with Snapchat Data Collection:
1. Most of the linkedin users in Nigeria do not post a lot about GBV experiences, and as such, data collected were too little to build a model on.
2. The [tool](https://phantombuster.com/automations/linkedin/3112/linkedin-profile-scraper) being used for downloading the content only allowed 100 profile scrapes per day, thus making scrapping a lengthy process

### Dataset Format
Excel sheet with details about the posts, the data posted, the profile owner's age, occupation, etc.