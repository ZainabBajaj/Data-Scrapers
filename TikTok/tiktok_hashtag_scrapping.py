!pip install playwright
!pip install TikTokApi
from TikTokApi import TikTokApi
import pandas as pd
from flatten_dict import flatten

api = TikTokApi()
n_videos = 10000
'''
hashtag_list = ['JusticeforJenifer', 'JusticeforUwa', 'MeToo', 'ArewaMeTo', 'gb', 'genderbasedviolence', 'domesticviolence', 
'endgbv', 'GBVNigeria', 'metoo', 'guidedbyvoices', 'stopgbv', 'consent', 'domesticabuse', 'arewametoo', 'sexualabuse', 
'sexualexploitation', 'sexualharassment', 'violenceagainstwomen', 'rape', 'sexualassault', 'humanrightsviolation', 'SpotlightEndViolence', 'SpotlightNG']
'''
hashtag_list = ['justiceforuwa', 'justiceforjennifer', 'metoo', 'gbv', 'genderbasedviolence', 'endgbv']

res = pd.DataFrame()
for hashtag in hashtag_list:
	hashtag_videos = api.byHashtag(hashtag, count = n_videos)
	print(len(hashtag_videos))

	current_res = pd.DataFrame()
	for video in hashtag_videos:
		video = flatten(video, reducer = 'path')
		video_id, author = video['id'], video['author/uniqueId']
		df = pd.DataFrame([video])
		df['hashtag'] = hashtag
		df['video/url'] = 'https://www.tiktok.com/@' + str(author) + '/video/' + str(video_id)
		current_res = current_res.append(df)

	print(hashtag, current_res.shape)
	res = res.append(current_res)
print(res.shape)
res.to_excel("tiktok_video_by_hashtag_1.xlsx", index = False)
