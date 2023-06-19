#libraries
import pandas as pd
from IPython.display import clear_output
from bs4 import BeautifulSoup
import requests
from youtube_transcript_api import YouTubeTranscriptApi

#loading the links which were scrapped
df = pd.read_csv('https://raw.githubusercontent.com/MohitChoudhary23/Sales-Prediction/main/links.csv')
#list of links
links = list(df['Links'])
video_title = []
video_date = []
ans=0
links2 = []

#scrapping title , date for each url using BeautifulSoup
for i in range(len(links)):
    link = links[i]
    if link[:5] == 'https':
      response = requests.get(link)
      soup = BeautifulSoup(response.text, "html.parser")

      titleSoupMeta = soup.find("meta", property="og:title")
      videoTitle = titleSoupMeta["content"] if titleSoupMeta else "NotFound"

      titleSoupMeta = soup.find("meta", itemprop="datePublished")
      date = titleSoupMeta["content"] if titleSoupMeta else "NotFound"
      
      video_title.append(videoTitle)
      video_date.append(date)
      ans+=1
      links2.append(links[i])
#list of links, video_title, video_date

links = links2.copy()
video_title
video_date
# remove the video urls which are before 2020 year
final_links = []
for i in range(len(links)):
  if int(video_date[i][:4]) >= 2020:
    final_links.append([video_title[i] , video_date[i], links[i]])

#getting the ID of each URL

links_video_id = []
for i in range(len(links)):
    temp = links[i]
    a,b=temp.split('=')
    links_video_id.append(b)


list_with_transcripts = []

# iterating through every links_video_id and scrapping auto generated transcripts for all the videos

for i in range(len(links_video_id)):
    video_id = links_video_id[i]
    try:
        l = YouTubeTranscriptApi.get_transcript(video_id,languages=['en'])
        #if transcript is not availble it throws an error so try and except can avoid that
    except Exception:
        continue
    s=''
    for j in l:
        s+=j['text']
        s+=' '
    print(i)
    list_with_transcripts.append([video_title[i],video_date[i],links[i],s])

#loading title,date,link,transcript in csv file(transcripts_csv)

transcripts_csv = pd.DataFrame(list_with_transcripts,columns=['title','date','link','transcript'])

transcripts_csv.to_csv('yt_transcripts.csv')
